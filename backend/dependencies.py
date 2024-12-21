# 앱 의존성 관련 로직 파일
import torch
from loguru import logger

from model.model import BaseModel

model = None

""" [To-do]
- [] Error handler : Checkpoint's path
- [] Error handler :
"""

# Load model using checkpoint
def load_model(model_path: str) -> None:
    global model

    # Step1. Load model
    logger.info(f"Loading model from {model_path}.")
    device = torch.device("cpu")

    # Step2. Check if checkpoint is TRUE(valid)
    logger.info("Model loaded.")