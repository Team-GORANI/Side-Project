import torch
import cv2
import sqlite3
from pathlib import Path
from ultralytics import YOLO
import argparse

# Define labels for each category
CATEGORY_LABELS = {
    "house": [
        "집전체", "지붕", "집벽", "문", "창문", "굴뚝", "연기", "울타리", "길", "연못",
        "산", "나무", "꽃", "잔디", "태양"
    ],
    "person": [
        "사람전체", "머리", "얼굴", "눈", "코", "입", "귀", "머리카락", "목", "상체",
        "팔", "손", "다리", "발", "단추", "주머니", "운동화", "구두"
    ],
    "tree": [
        "나무전체", "기둥", "수관", "가지", "뿌리", "나뭇잎", "꽃", "열매", "그네", "새",
        "다람쥐", "구름", "달", "별"
    ]
}

def create_database(db_path):
    """데이터베이스와 테이블 생성"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # detections 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            w INTEGER NOT NULL,
            h INTEGER NOT NULL,
            img_id TEXT NOT NULL
        )
    ''')

    conn.commit()
    return conn

def infer_and_save(image_path, category):
    # Validate category
    if category not in CATEGORY_LABELS:
        raise ValueError(f"Invalid category '{category}'. Choose from {list(CATEGORY_LABELS.keys())}.")

    # Load model and labels
    model_path = CATEGORY_MODELS[category]
    labels = CATEGORY_LABELS[category]
    model = YOLO(model_path)

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img_name = Path(image_path).stem

    # Automatically set output path
    db_path = f"output_{category}_{img_name}.db"

    # Create DB table
    conn = create_database(db_path)
    c = conn.cursor()

    # Inference
    results = model(image_path)

    # Extract detections
    detections = results[0].boxes
    boxes = detections.xyxy.cpu().numpy()
    classes = detections.cls.cpu().numpy().astype(int)

    # Build annotations
    for box, cls in zip(boxes, classes):
        x1, y1, x2, y2 = box
        label = labels[cls] if cls < len(labels) else "Unknown"

        # DB에 데이터 삽입
        c.execute('''
            INSERT INTO detections (label, x, y, w, h, img_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            label,
            int(x1),
            int(y1),
            int(x2 - x1),
            int(y2 - y1),
            img_name
        ))

    # 변경사항 저장 및 연결 종료
    conn.commit()
    conn.close()

    print(f"Results saved to {db_path}")

def main():
    parser = argparse.ArgumentParser(description="Unified Inference Script")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image")
    parser.add_argument("--category", type=str, required=True, choices=CATEGORY_LABELS.keys(),
                        help="Category of the model to use (e.g., 'house', 'person', 'tree')")
    args = parser.parse_args()

    infer_and_save(args.image, args.category)

if __name__ == "__main__":
    main()
