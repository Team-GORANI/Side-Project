from ultralytics import YOLO

person_model = YOLO("models/person_model.pt")

def detect_people(image_path: str) -> list:
    """
    사람 객체 탐지를 수행하고 결과 반환
    """
    results = person_model(image_path)
    return results[0].boxes.data.tolist()