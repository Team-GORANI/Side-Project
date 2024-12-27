import os
from fastapi import APIRouter, HTTPException, status, UploadFile
from pydantic import BaseModel
from PIL import Image

# Custom : Import from other files
from model.inference import infer_and_save
from config import Config
from tools.htp_analyzer import analyze_with_gpt

router = APIRouter()

# Pydantic : Type validation
class PredictionResponse(BaseModel):
    id: int
    result: int


# FastAPI 경로
@router.post("/predict")
async def predict(file: UploadFile) -> PredictionResponse:
    # Step1. 이미지를 임시 파일로 저장
    content = await file.read()
    image_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)

    with open(image_path, "wb") as f:
        f.write(content)

    # Step2. Inference(predict) using ckpt

    # Step3. Create info using object_func.py

    # Step4. Create HTP result using htp_analyzer.py

    # Step5. 임시 파일 삭제

    # Step6. Type Validation : id (In, Out)

    yield