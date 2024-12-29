from ultralytics import YOLO

tree_model = YOLO("models/tree_model.pt")

def detect_trees(image_path: str) -> list:
    """
    나무 객체 탐지를 수행하고 결과 반환
    """
    results = tree_model(image_path)
    return results[0].boxes.data.tolist()