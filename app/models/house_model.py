from ultralytics import YOLO

house_model = YOLO("models/house_model.pt")

def detect_houses(image_path: str) -> list:
    """
    집 객체 탐지를 수행하고 결과 반환
    """
    results = house_model(image_path)
    return results[0].boxes.data.tolist()