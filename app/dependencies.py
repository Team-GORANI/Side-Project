from app.models.house_model import detect_houses
from app.models.tree_model import detect_trees
from app.models.person_model import detect_people

def get_model_predictions(image_path: str) -> dict:
    """
    각각의 YOLOv8n 모델을 호출하여 탐지 결과를 병합
    """
    house_results = detect_houses(image_path)
    tree_results = detect_trees(image_path)
    person_results = detect_people(image_path)

    combined_results = {
        "houses": house_results,
        "trees": tree_results,
        "person": person_results,
    }
    return combined_results