## GPT로 이용해 간단하게 코드만든거 

from fastapi import APIRouter, HTTPException, status, UploadFile
from pydantic import BaseModel
from sqlmodel import Session
from PIL import Image
import torch
from ultralytics import YOLO

from database import DetectionResult, engine
from dependencies import get_model  # 모델 로드 함수

router = APIRouter()


class DetectionResponse(BaseModel):
    id: int
    detections: list  # [ {class_id: int, confidence: float, bbox: list} ]


# FastAPI 경로
@router.post("/detect")
def detect(file: UploadFile) -> DetectionResponse:
    # 이미지 파일과 사이즈가 맞는지 검증
    try:
        image = Image.open(file.file)
        if image.mode != "RGB":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="이미지는 RGB 모드여야 합니다."
            )
        if image.size[0] < 32 or image.size[1] < 32:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="이미지 크기는 최소 32x32 이상이어야 합니다."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"이미지 파일이 유효하지 않습니다: {str(e)}"
        )

    # 모델 로드 및 추론
    model: YOLO = get_model()  # YOLO 모델 로드
    try:
        results = model(image)  # 이미지에서 탐지 수행
        detections = []
        for result in results[0].boxes:
            detections.append({
                "class_id": int(result.cls),  # 탐지된 클래스 ID
                "confidence": float(result.conf),  # 탐지 확률
                "bbox": [float(coord) for coord in result.xyxy]  # 바운딩 박스 좌표 (x1, y1, x2, y2)
            })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"모델 추론 중 오류가 발생했습니다: {str(e)}"
        )

    # 결과를 데이터베이스에 저장 (DetectionResult 사용)
    detection_result = DetectionResult(detections=detections)
    with Session(engine) as session:
        session.add(detection_result)
        session.commit()
        session.refresh(detection_result)

    # 응답하기
    return DetectionResponse(id=detection_result.id, detections=detections)