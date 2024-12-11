import torch
import cv2
import json
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

CATEGORY_MODELS = {
    "house": "./best_house.pt",
    "person": "./best_person.pt",
    "tree": "./best_tree.pt"
}

# Inference function
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
    output_path = f"output_{category}_{img_name}.json"

    # Inference
    results = model(image_path)

    # Extract detections
    detections = results[0].boxes  # Directly access the Boxes object
    boxes = detections.xyxy.cpu().numpy()  # [x1, y1, x2, y2] coordinates
    confs = detections.conf.cpu().numpy()  # Confidence scores
    classes = detections.cls.cpu().numpy().astype(int)  # Class indices

    # Build annotations
    annotations = {
        "anno_id": "unique_annotation_id",  # Replace with actual ID generator if needed
        "class": category,  # Add category as class in annotations
        "bbox_count": len(boxes),
        "bbox": []
    }

    for box, conf, cls in zip(boxes, confs, classes):
        x1, y1, x2, y2 = box
        label = labels[cls] if cls < len(labels) else "Unknown"
        annotations["bbox"].append({
            "label": label,
            "x": int(x1),
            "y": int(y1),
            "w": int(x2 - x1),
            "h": int(y2 - y1)
        })

    # Build meta data
    meta = {
        "img_id": img_name,
        "contributor": "",
        "date_created": "",
        "img_path": image_path,
        "label_path": "",
        "img_size": img.size if img is not None else 0,
        "img_resolution": f"{img.shape[1]}x{img.shape[0]}" if img is not None else "",
        "age": "",
        "sex": ""
    }

    # Combine results
    result = {
        "meta": meta,
        "annotations": annotations,
    }

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Results saved to {output_path}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Unified Inference Script")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image")
    parser.add_argument("--category", type=str, required=True, choices=CATEGORY_LABELS.keys(),
                        help="Category of the model to use (e.g., 'house', 'person', 'tree')")
    args = parser.parse_args()

    infer_and_save(args.image, args.category)

if __name__ == "__main__":
    main()