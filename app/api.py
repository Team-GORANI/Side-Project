from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Union
import logging
import os
import requests  # Ollama API 호출용

from database import save_to_database, SessionLocal, DetectionResult
from models.house_model import detect_houses
from models.tree_model import detect_trees
from models.person_model import detect_people
from models.house_func import analyze_house
from models.person_func import analyze_person
from models.tree_func import analyze_tree

# 로깅 설정
logger = logging.getLogger(__name__)

router = APIRouter()

##############################
# Logger, Label 관련 코드
##############################

# 커스텀 예외 클래스
class ImageProcessingError(Exception):
    """이미지 처리 중 발생하는 에러"""
    pass

class DatabaseError(Exception):
    """데이터베이스 작업 중 발생하는 에러"""
    pass

# house label
house_label = {
    0: "집전체", 1: "지붕", 2: "집벽", 3: "문", 4: "창문",
    5: "굴뚝", 6: "연기", 7: "울타리", 8: "길", 9: "연못",
    10: "산", 11: "나무", 12: "꽃", 13: "잔디", 14: "태양"
}

# person label
person_label = {
    0: "사람전체", 1: "머리", 2: "얼굴", 3: "눈", 4: "코",
    5: "입", 6: "귀", 7: "머리카락", 8: "목", 9: "상체",
    10: "팔", 11: "손", 12: "다리", 13: "발", 14: "단추",
    15: "주머니", 16: "운동화", 17: "남자구두"
}

# tree label
tree_label = {
    0: "나무전체", 1: "기둥", 2: "수관", 3: "가지", 4: "뿌리",
    5: "나뭇잎", 6: "꽃", 7: "열매", 8: "그네", 9: "새",
    10: "다람쥐", 11: "구름", 12: "달", 13: "별"
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

    @validator('image_type')
    def validate_image_type(cls, v):
        if v.lower() not in ["house", "tree", "person"]:
            raise ValueError("image_type은 house, tree, person 중 하나여야 합니다.")
        return v.lower()

    @validator('image_path')
    def validate_image_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"이미지 파일을 찾을 수 없습니다: {v}")
        return v

def parse_bboxes(yolo_raw_boxes: List[List[float]], image_type: str) -> List[Dict]:
    """
    YOLO 결과값을 받아 (h, w, x, y) 형태로 변환해주는 헬퍼 함수.
    YOLO는 일반적으로 [x1, y1, x2, y2, confidence, class_id] 형태로 배열을 반환한다고 가정.
    """
    try:
        parsed = []
        for bbox in yolo_raw_boxes:
            try:
                # 예) bbox = [x1, y1, x2, y2, confidence, label]
                x1, y1, x2, y2 = bbox[:4]
                w = x2 - x1
                h = y2 - y1

                if image_type == "house":
                    label_map = house_label
                elif image_type == "person":
                    label_map = person_label
                elif image_type == "tree":
                    label_map = tree_label

                parsed.append({
                    "x": float(x1),
                    "y": float(y1),
                    "w": float(w),
                    "h": float(h),
                    "confidence": float(bbox[4]),
                    "label": label_map[int(bbox[5])]
                })
            except Exception as e:
                logger.error(f"Error parsing bbox: {e}")
                continue

        return parsed
    except Exception as e:
        raise ImageProcessingError(f"바운딩 박스 파싱 중 에러 발생: {str(e)}")

@router.post("/detect")
async def detect_objects(request: ImageRequest):
    """
    1) image_type을 보고 해당 YOLO 모델 사용 (house/tree/person)
    2) 탐지 결과의 bbox를 (h, w, x, y) 형태로 파싱
    3) DB에 저장
    4) 결과를 반환
    """
    try:
        image_type = request.image_type
        image_path = request.image_path

        # 모델 선택 및 객체 탐지
        if image_type == "house":
            raw_results = detect_houses(image_path)
        elif image_type == "tree":
            raw_results = detect_trees(image_path)
        elif image_type == "person":
            raw_results = detect_people(image_path)
        else:
            raise ValueError("image_type은 house, tree, person 중 하나여야 합니다.")

        # 결과 파싱 및 저장
        parsed_results = parse_bboxes(raw_results, image_type)
        detection_data = {image_type: parsed_results}

        try:
            save_to_database(image_path, detection_data)
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError("결과를 데이터베이스에 저장하는 중 에러가 발생했습니다.")

        return {
            "status": "success",
            "image_path": image_path,
            "results": detection_data
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ImageProcessingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="예상치 못한 에러가 발생했습니다."
        )

##############################
# 2) Ollama 분석 관련 코드
##############################

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama 기본 API 엔드포인트

@router.get("/analysis/{image_path:path}")
async def analyze_image(image_path: str):
    """
    1) DB에서 image_path에 해당하는 탐지 결과 조회
    2) 탐지 결과(예: house, tree, person 각각의 bbox) 분석
    3) Ollama API를 통해 HTP 해석 프롬프트 전송
    4) 결과 반환
    """
    try:
        # 1) DB에서 결과 조회
        session = SessionLocal()
        try:
            db_entry = session.query(DetectionResult).filter_by(image_path=image_path).first()
            if not db_entry:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"해당 {image_path}가 DB에 없습니다."
                )
            detection_data = db_entry.results
        finally:
            session.close()

        # 2) '크다/작다' 간단 분석
        feature_list = []
        for cls_name, bboxes in detection_data.items():
            if cls_name == "house":
                house_results = analyze_house(bboxes)
                feature_list.extend(house_results)
            elif cls_name == "person":
                person_results = analyze_person(bboxes)
                feature_list.extend(person_results)
            elif cls_name == "tree":
                tree_results = analyze_tree(bboxes)
                feature_list.extend(tree_results)

        # Ollama에 전달할 프롬프트 생성
        drawing_type = "HTP"
        if "house" in image_path.lower():
            drawing_type = "house"
        elif "tree" in image_path.lower():
            drawing_type = "tree"
        elif "person" in image_path.lower():
            drawing_type = "person"

        features_str = "\n".join(feature_list)

        # Ollama API 요청
        prompt = f"""당신은 전문적인 HTP 심리 상담가입니다.

        분석할 그림 유형: {drawing_type.upper()}
        탐지된 특징들:
        {features_str}

        위 특징들을 바탕으로 다음 구조로 분석해주세요:

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

        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "llama2",  # 또는 다른 설치된 모델
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ollama API 호출 중 에러가 발생했습니다."
            )

        analysis_result = response.json()["response"]

        return {
            "status": "success",
            "features_analyzed": feature_list,
            "analysis_result": analysis_result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"분석 중 예상치 못한 에러: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="분석 중 예상치 못한 에러가 발생했습니다."
        )
