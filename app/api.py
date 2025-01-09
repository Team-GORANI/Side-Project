import os
import socket

import requests
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from models.house_func import analyze_house
from models.house_model import detect_houses
from models.person_func import analyze_person
from models.person_model import detect_people
from models.tree_func import analyze_tree
from models.tree_model import detect_trees

router = APIRouter()

# Ollama 설정
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:11434"
print(f"Configured Ollama URL: {OLLAMA_BASE_URL}")


# 디버깅을 위한 연결 체크 함수
def check_ollama_connection():
    try:
        # DNS 확인 시도
        ip_address = socket.gethostbyname(OLLAMA_HOST)
        print(f"Resolved {OLLAMA_HOST} to {ip_address}")

        # HTTP 연결 테스트
        test_url = f"http://{OLLAMA_HOST}:11434/api/version"
        response = requests.get(test_url, timeout=5)
        print(f"Ollama version check: {response.status_code}")
        return True
    except socket.gaierror as e:
        print(f"DNS resolution failed for {OLLAMA_HOST}: {str(e)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Connection test failed: {str(e)}")
        return False


# Label 정의
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
    14: "태양",
}

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
    17: "구두",
}

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
    13: "별",
}


class ImageRequest(BaseModel):
    """이미지 요청을 위한 모델"""

    image_type: str
    image_path: str


def parse_bboxes(yolo_raw_boxes, image_type):
    """YOLO 결과값을 바운딩 박스로 변환"""
    parsed = []
    for bbox in yolo_raw_boxes:
        x1, y1, x2, y2 = bbox[:4]
        w = x2 - x1
        h = y2 - y1
        base_data = {
            "x": float(x1),
            "y": float(y1),
            "w": float(w),
            "h": float(h),
            "confidence": float(bbox[4]),
        }

        if image_type == "house":
            base_data["label"] = house_label[int(bbox[5])]
        elif image_type == "person":
            base_data["label"] = person_label[int(bbox[5])]
        elif image_type == "tree":
            base_data["label"] = tree_label[int(bbox[5])]

        parsed.append(base_data)
    return parsed


@router.post("/detect")
async def detect_image(image: UploadFile = File(...), type: str = Form(...)):
    """이미지 객체 감지 엔드포인트"""
    try:
        # 임시 파일로 저장
        contents = await image.read()
        image_path = f"temp/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(contents)

        try:
            # 객체 감지 수행
            detection_map = {
                "house": (detect_houses, analyze_house, house_label),
                "tree": (detect_trees, analyze_tree, tree_label),
                "person": (detect_people, analyze_person, person_label),
            }

            if type not in detection_map:
                return {"status": "error", "message": "Invalid type"}

            detect_func, analyze_func, label_dict = detection_map[type]
            boxes = detect_func(image_path)

            # boxes 형식 검증 및 변환
            if isinstance(boxes, list):
                formatted_boxes = [
                    {
                        "label": label_dict[int(box[5])],
                        "x": float(box[0]),
                        "y": float(box[1]),
                        "w": float(box[2] - box[0]),
                        "h": float(box[3] - box[1]),
                    }
                    for box in boxes
                ]

                # YOLO 분석
                yolo_analysis = analyze_func(formatted_boxes)

                # Ollama 분석
                ollama_result = await analyze_drawing(image_path, formatted_boxes, type)

                # 분석 결과 처리
                analysis_text = (
                    ollama_result.get("ollama_result")
                    if ollama_result and "ollama_result" in ollama_result
                    else yolo_analysis
                    if isinstance(yolo_analysis, str)
                    else "\n".join(yolo_analysis)
                )
            else:
                analysis_text = f"No {type} objects detected"

            # 임시 파일 삭제
            if os.path.exists(image_path):
                os.remove(image_path)

            return {
                "status": "success",
                "analysis": analysis_text,
                "boxes": formatted_boxes,
            }

        except Exception as analysis_error:
            print(f"Analysis error: {str(analysis_error)}")
            if os.path.exists(image_path):
                os.remove(image_path)
            return {
                "status": "error",
                "message": "이미지 분석 중 오류가 발생했습니다.",
                "error": str(analysis_error),
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.get("/analysis/{image_path:path}")
async def analyze_drawing(image_path: str, boxes: list, type: str):
    """Ollama를 사용한 심리 분석"""
    # 연결 테스트
    if not check_ollama_connection():
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to Ollama service at {OLLAMA_BASE_URL}",
        )

    try:
        # 특징 분석
        analyze_funcs = {
            "house": analyze_house,
            "tree": analyze_tree,
            "person": analyze_person,
        }

        feature_list = []
        if type in analyze_funcs:
            feature_list.extend(analyze_funcs[type](boxes))

        features_str = "\n".join(feature_list)

        system_prompt = """
        You are a professional HTP psychologist and mental health counselor.
        Analyze both current psychological state and developmental influences through drawing features.
        Provide detailed analysis by connecting specific drawing features to psychological interpretations.
        - Use formal Korean (-습니다)
        - Do not use special characters
        - Avoid using personal pronouns or labels (e.g., 'you', 'artist', etc)
        - Only use emojis that are specifically defined in section headers
        """

        user_prompt = f"""
        === HTP Analysis Request ===
        Drawing Type: {type.upper()}
        Features Detected:
        {features_str}

        Using the bounding box coordinates, analyze the sketch and provide psychological interpretation in Korean.
        Translate all measurements into descriptive terms (e.g., centered, upper right, small):

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

        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": "mistral:7b-q4",
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                    "temperature": 0.5,
                },
                timeout=30,
            )
            response.raise_for_status()
            analysis_text = response.json()["response"]

            return {
                "status": "success",
                "features_analyzed": feature_list,
                "ollama_result": analysis_text,
            }

        except requests.exceptions.RequestException as e:
            print(f"Ollama API error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Ollama API 호출 중 오류가 발생했습니다: {str(e)}",
            )

    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
