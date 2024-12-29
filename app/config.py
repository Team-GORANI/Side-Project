import os

# YOLOv8n 모델 경로
MODEL_PATHS = {
    "house": os.getenv("HOUSE_MODEL_PATH", "models/house_model.pt"),
    "tree": os.getenv("TREE_MODEL_PATH", "models/tree_model.pt"),
    "person": os.getenv("PERSON_MODEL_PATH", "models/person_model.pt"),
}

# 데이터베이스 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///htp_project.db")