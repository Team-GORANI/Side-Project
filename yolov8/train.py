import torch
from tqdm import tqdm
from ultralytics import YOLO
import os
import json


def convert_to_yolo(json_path, output_dir):
    # JSON 파일 읽기
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이미지 크기 가져오기
    resolution = data['meta']['img_resolution']
    img_width, img_height = map(int, resolution.split('x'))

    # YOLO 라벨 파일 생성
    yolo_labels = []
    for bbox in data['annotations']['bbox']:
        label = bbox['label']
        if label not in CLASS_NAMES:
            continue  # 정의되지 않은 클래스는 무시

        class_id = CLASS_NAMES[label]
        x_center = (bbox['x'] + bbox['w'] / 2) / img_width
        y_center = (bbox['y'] + bbox['h'] / 2) / img_height
        width = bbox['w'] / img_width
        height = bbox['h'] / img_height

        yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # YOLO 라벨 파일 저장
    img_path = data['meta']['img_path']
    img_name = os.path.basename(img_path).replace('.jpg', '.txt')  # 이미지 파일 이름에서 확장자를 .txt로 변경
    output_path = os.path.join(output_dir, img_name)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(yolo_labels))

CLASS_NAMES = {
    "집전체": 0,
    "지붕": 1,
    "집벽": 2,
    "문": 3,
    "창문": 4,
    "굴뚝": 5,
    "연기": 6,
    "울타리": 7,
    "길": 8,
    "연못": 9,
    "산": 10,
    "나무": 11,
    "꽃": 12,
    "잔디": 13,
    "태양": 14
}


# json_dir = "C:/Users/Windows/Desktop/Side_Project/data/house/train/label"
# output_dir = "C:/Users/Windows/Desktop/Side_Project/data/house/train/image"
# json_dir = "C:/Users/Windows/Desktop/Side_Project/data/house/val/label"
# output_dir = "C:/Users/Windows/Desktop/Side_Project/data/house/val/image"

# os.makedirs(output_dir, exist_ok=True)

# for json_file in os.listdir(json_dir):
#     if json_file.endswith(".json"):
#         convert_to_yolo(os.path.join(json_dir, json_file), output_dir)


# YOLOv8 모델 로드 (사전 학습된 모델을 사용)
model = YOLO('yolov8x.pt')
data_yaml = "C:/Users/Windows/Desktop/Side_Project/yolov8/data.yaml"  # data.yaml 파일 경로

# 학습 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Optimizer 설정

best_val_loss = float('inf')  # 초기 best_val_loss를 무한대로 설정

model.train(
        data=data_yaml, 
        epochs=100, 
        imgsz=1280,  
        batch=8,
        optimizer='AdamW',  # 옵티마이저를 AdamW로 설정
        lr0=1e-4
        )

    # 학습
    
 
