from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

from openai import OpenAI
from database import save_to_database, SessionLocal, DetectionResult
from models.house_model import detect_houses
from models.tree_model import detect_trees
from models.person_model import detect_people

# 분석 함수 매핑
from models.house_func import analyze_house
from models.person_func import analyze_person
from models.tree_func import analyze_tree

router = APIRouter()

# house label
house_label = {
    0: "집전체",
    1: "지붕",
    2: "집벽",
    3: "문",
    4: "창문",
    5: "굴뚝",
    6: "연기",
    7: "울타리",
    8: "길",
    9: "연못",
    10: "산",
    11: "나무",
    12: "꽃",
    13: "잔디",
    14: "태양"
}

# person label
person_label = {
    0: "사람전체",
    1: "머리",
    2: "얼굴",
    3: "눈",
    4: "코",
    5: "입",
    6: "귀",
    7: "머리카락",
    8: "목",
    9: "상체",
    10: "팔",
    11: "손",
    12: "다리",
    13: "발",
    14: "단추",
    15: "주머니",
    16: "운동화",
    17: "구두"
}

# tree label
tree_label = {
    0: "나무전체",
    1: "기둥",
    2: "수관",
    3: "가지",
    4: "뿌리",
    5: "나뭇잎",
    6: "꽃",
    7: "열매",
    8: "그네",
    9: "새",
    10: "다람쥐",
    11: "구름",
    12: "달",
    13: "별"
}

##############################
# 1) YOLO 객체 탐지 관련 코드
##############################

class ImageRequest(BaseModel):
    """
    image_type: "house", "tree", 또는 "person"
    image_path: 실제 이미지 파일 경로
    """
    image_type: str
    image_path: str

def parse_bboxes(yolo_raw_boxes, image_type):
    """
    YOLO 결과값을 받아 (h, w, x, y) 형태로 변환해주는 헬퍼 함수.
    YOLO는 일반적으로 [x1, y1, x2, y2, confidence, class_id] 형태로 배열을 반환한다고 가정.
    """
    parsed = []
    for bbox in yolo_raw_boxes:
        # 예) bbox = [x1, y1, x2, y2, confidence, label]
        x1, y1, x2, y2 = bbox[:4]
        w = x2 - x1
        h = y2 - y1
        if image_type == "house":
            parsed.append({
                "x": float(x1),
                "y": float(y1),
                "w": float(w),
                "h": float(h),
                "confidence": float(bbox[4]),
                "label": house_label[int(bbox[5])]
            })
        elif image_type == "person":
            parsed.append({
                "x": float(x1),
                "y": float(y1),
                "w": float(w),
                "h": float(h),
                "confidence": float(bbox[4]),
                "label": person_label[int(bbox[5])]
            })
        elif image_type == "tree":
            parsed.append({
                "x": float(x1),
                "y": float(y1),
                "w": float(w),
                "h": float(h),
                "confidence": float(bbox[4]),
                "label": tree_label[int(bbox[5])]
            })
    return parsed

@router.post("/detect")
async def detect_image(
    image: UploadFile = File(...),
    type: str = Form(...)
):
    try:
        # 임시 파일로 저장
        contents = await image.read()
        image_path = f"temp/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(contents)
        
        try:
            formatted_boxes = []
            
            # 객체 감지 수행
            if type == "house":
                boxes = detect_houses(image_path)
                detect_func = analyze_house
                label_dict = house_label 
            elif type == "tree":
                boxes = detect_trees(image_path)
                detect_func = analyze_tree
                label_dict = tree_label
            elif type == "person":
                boxes = detect_people(image_path)
                detect_func = analyze_person
                label_dict = person_label
            else:
                return {"status": "error", "message": "Invalid type"}

            # boxes 형식 검증 및 변환
            if isinstance(boxes, list):
                formatted_boxes = [
                    {
                        "label": label_dict[int(box[5])],
                        "x": float(box[0]),
                        "y": float(box[1]),
                        "w": float(box[2] - box[0]),
                        "h": float(box[3] - box[1])
                    }
                    for box in boxes
                ]
                
                # YOLO 분석
                yolo_analysis = detect_func(formatted_boxes)
                
                # GPT 분석
                gpt_result = await analyze_drawing(image_path, formatted_boxes, type)
                
                # 분석 결과 처리
                if gpt_result and "gpt_result" in gpt_result:
                    analysis_text = gpt_result["gpt_result"]
                else:
                    analysis_text = yolo_analysis if isinstance(yolo_analysis, str) else "\n".join(yolo_analysis)

            else:
                analysis_text = f"No {type} objects detected"

            # 임시 파일 삭제
            if os.path.exists(image_path):
                os.remove(image_path)

            return {
                "status": "success",
                "analysis": analysis_text,
                "boxes": formatted_boxes
            }

        except Exception as analysis_error:
            print(f"Analysis error: {str(analysis_error)}")
            if os.path.exists(image_path):
                os.remove(image_path)
            return {
                "status": "error",
                "message": "이미지 분석 중 오류가 발생했습니다.",
                "error": str(analysis_error)
            }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}

##############################
# 2) GPT 분석 관련 코드
##############################
from dotenv import load_dotenv
load_dotenv() 

# OpenAI API 키 설정 수정
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@router.get("/analysis/{image_path:path}")
async def analyze_drawing(image_path: str, boxes: list, type: str):
    """
    1) 탐지 결과 분석
    2) GPT API를 통해 HTP 해석 프롬프트 전송
    3) 결과 반환
    """
    try:
        # 특징 분석
        feature_list = []
        
        # 각 타입별 분석 수행
        if type == "house":
            feature_list.extend(analyze_house(boxes))
        elif type == "tree":
            feature_list.extend(analyze_tree(boxes))
        elif type == "person":
            feature_list.extend(analyze_person(boxes))

        # GPT에 전달할 문자열 생성
        features_str = "\n".join(feature_list)

        # system_prompt (기존 코드 유지)
        system_prompt = """You are a professional HTP psychologist and mental health counselor.
        Analyze both current psychological state and developmental influences through drawing features.
        Provide detailed analysis by connecting specific drawing features to psychological interpretations. 
        - Use formal Korean (-습니다)
        - Do not use special characters
        - Avoid using personal pronouns or labels (e.g., 'you', 'artist', etc)
        - Only use emojis that are specifically defined in section headers
        """

        # user_prompt (기존 코드 유지)
        user_prompt = f"""
        === HTP Analysis Request ===
        Drawing Type: {type.upper()}
        Features Detected:
        {features_str}

        Using the bounding box coordinates [x,y,w,h], analyze the sketch and provide psychological interpretation in formal Korean.
        Translate all measurements into descriptive terms (e.g., centered, upper right, large, small):

        1. Personality Analysis:
        - Start with "1. 🔅 성격 특징 🔅"
        - Key personality traits
        - Analyze element sizes and placements from coordinates
        - Connect spatial features to personality traits
        - Interpret overall composition

        2. Social Characteristics:
        - Start with "2. 🌤️ 대인 관계 🌤️"
        - Family relationship patterns
        - Communication style
        - Interpret element spacing and relationship boundaries
        - Attachment patterns

        3. Current Mental State:
        - Start with "3. 🧘 현재 심리 상태 🧘"
        - Emotional stability
        - Developmental effects
        - Stress/anxiety levels
        - Coping mechanisms

        4. Mental Health Care:
        - Start with "4. 💪 멘탈 케어 Tips 💪"
        - Understanding past influences
        - Stress management suggestions
        - Provide practical suggestions
        - Growth potential
        """

        # (3-3) 최신 openai >= 1.0.0 방식
        # ChatCompletion → "openai.chat_completions.create(...)"
        # 또는 그대로 openai.ChatCompletion.create(...)가 동작하는 경우도 있으나,
        # 최신 권장 방식은 아래와 같습니다.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 공식 OpenAI 모델 사용 (ex: gpt-3.5-turbo or gpt-4)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            presence_penalty=0.3
        )

        gpt_answer = response.choices[0].message.content.strip()

        return {
            "status": "success",
            "features_analyzed": feature_list,
            "gpt_result": gpt_answer
        }

    except Exception as e:
        print(f"GPT Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))