from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from openai import OpenAI
from app.database import save_to_database, SessionLocal, DetectionResult
from app.models.house_model import detect_houses
from app.models.tree_model import detect_trees
from app.models.person_model import detect_people

# 분석 함수 매핑
from app.models.house_func import analyze_house
from app.models.person_func import analyze_person
from app.models.tree_func import analyze_tree

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
    17: "남자구두"
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
                "label": tree_labe[int(bbox[5])]
            })
    return parsed

@router.post("/detect")
async def detect_objects(request: ImageRequest):
    """
    1) image_type을 보고 해당 YOLO 모델 사용 (house/tree/person)
    2) 탐지 결과의 bbox를 (h, w, x, y) 형태로 파싱
    3) DB에 저장
    4) 결과를 반환
    """
    try:
        image_type = request.image_type.lower()
        image_path = request.image_path

        if image_type == "house":
            raw_results = detect_houses(image_path)
            parsed_results = parse_bboxes(raw_results, image_type)
        elif image_type == "tree":
            raw_results = detect_trees(image_path)
            parsed_results = parse_bboxes(raw_results, image_type)
        elif image_type == "person":
            raw_results = detect_people(image_path)
            parsed_results = parse_bboxes(raw_results, image_type)
        else:
            raise ValueError("image_type은 house, tree, person 중 하나여야 합니다.")

        detection_data = { image_type: parsed_results }

        save_to_database(image_path, detection_data)

        return {
            "status": "success",
            "image_path": image_path,
            "results": detection_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##############################
# 2) GPT 분석 관련 코드
##############################

# (1) OpenAI API 키 설정 (실제 서비스 시 보안을 위해 환경변수 사용 권장)
api_key = "your_api_key"
client = OpenAI(api_key=api_key)

@router.get("/analysis/{image_path:path}")
async def analyze_image(image_path: str):
    """
    1) DB에서 image_path에 해당하는 탐지 결과 조회
    2) 탐지 결과(예: house, tree, person 각각의 bbox) 분석: 바운딩 박스 면적이 큰지 작은지 등
    3) GPT API를 통해 HTP 해석 프롬프트 전송
    4) 결과 반환
    """
    try:
        # 1) DB에서 결과 조회
        session = SessionLocal()
        db_entry = session.query(DetectionResult).filter_by(image_path=image_path).first()
        session.close()

        if not db_entry:
            raise HTTPException(status_code=404, detail=f"해당 {image_path}가 DB에 없습니다.")

        detection_data = db_entry.results

        # 2) '크다/작다' 간단 분석
        feature_list = []

        for cls_name, bboxes in detection_data.items():
            if cls_name == "house":
                # House 분석
                house_results = analyze_house(bboxes)  # bboxes는 DB에서 가져온 바운딩 박스 데이터
                feature_list.extend(house_results)

            elif cls_name == "person":
                # Person 분석
                person_results = analyze_person(bboxes)  # bboxes 전달
                feature_list.extend(person_results)

            elif cls_name == "tree":
                # Tree 분석
                tree_results = analyze_tree(bboxes)  # bboxes 전달
                feature_list.extend(tree_results)

        # GPT에 전달할 문자열 생성
        features_str = "\n".join(feature_list)

        # (3-1) system_prompt
        system_prompt = """You are a professional HTP psychologist and mental health counselor.
        Analyze both current psychological state and developmental influences through drawing features.
        Provide detailed analysis by connecting specific drawing features to psychological interpretations. 
        - Use formal Korean (-습니다)
        - Do not use special characters
        - Avoid using personal pronouns or labels (e.g., 'you', 'artist', etc)
        - Only use emojis that are specifically defined in section headers
        """

        # (3-2) user_prompt
        # 이미지 경로에 "house", "tree", "person" 문자열이 포함되면 그걸로 drawing_type을 결정
        drawing_type = "HTP"
        lower_path = image_path.lower()
        if "house" in lower_path:
            drawing_type = "house"
        elif "tree" in lower_path:
            drawing_type = "tree"
        elif "person" in lower_path:
            drawing_type = "person"

        user_prompt = f"""
        === HTP Analysis Request ===
        Drawing Type: {drawing_type.upper()}
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

        Analysis guidelines:
        - Start content immediately after each section title
        - Write clear and concise paragraphs
        - Translate coordinates into descriptive terms
        - Include practical advice
        - Maintain a supportive tone
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

        # 4) 최종 결과 반환
        return {
            "status": "success",
            "features_analyzed": feature_list,
            "gpt_result": gpt_answer
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))