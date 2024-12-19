## GPT로 이용해 간단하게 코드만든거 

import torch
from loguru import logger

from Ultralytics import YOLO

model = None


def load_model(model_path: str) -> None:
    global model
    logger.info(f"Loading model from {model_path}.")

    model = YOLO(model_path)
    device = torch.device("cpu")
    # model.load_state_dict(torch.load(model_path, map_location=device))

    logger.info("Model loaded.")


def get_model() -> YOLO:
    global model
    return model

