import json

# JSON 파일 경로 
json_file_path = "data/person_infomation.json"

def calculate_head_to_upper_ratio(bboxes):
    """
    머리 / 상체의 비율을 계산하고 결과를 반환하는 함수
    """
    head_area = None
    upper_body_area = None

    for bbox in bboxes:
        if bbox.get("label") == "머리":
            head_area = bbox["w"] * bbox["h"]
        elif bbox.get("label") == "상체":
            upper_body_area = bbox["w"] * bbox["h"]

    if head_area and upper_body_area and upper_body_area > 0:
        ratio = head_area / upper_body_area
        if ratio > 2.2925420:
            return f"머리 / 상체 값은 {ratio:.4f}로 큰 편입니다."
        elif ratio < 1.2819802:
            return f"머리 / 상체 값은 {ratio:.4f}로 작은 편입니다."
        else:
            return f"머리 / 상체 값은 {ratio:.4f}로 평균입니다."
    
    return "머리 또는 상체의 정보가 부족합니다."

def calculate_eye_to_face_ratio(bboxes):
    """
    눈 / 얼굴의 비율을 계산하고 결과를 반환하는 함수
    """
    eye_areas = []
    face_area = None

    for bbox in bboxes:
        if bbox.get("label") == "눈":
            eye_areas.append(bbox["w"] * bbox["h"])
        elif bbox.get("label") == "얼굴":
            face_area = bbox["w"] * bbox["h"]

    if len(eye_areas) == 2 and face_area and face_area > 0:
        avg_eye_area = sum(eye_areas) / 2
        ratio = avg_eye_area / face_area
        if ratio > 0.0427861542:
            return f"눈 / 얼굴 값은 {ratio:.4f}로 큰 편입니다."
        elif ratio < 0.0221859051:
            return f"눈 / 얼굴 값은 {ratio:.4f}로 작은 편입니다."
        else:
            return f"눈 / 얼굴 값은 {ratio:.4f}로 평균입니다."
    
    return "눈 또는 얼굴의 정보가 부족합니다."

def calculate_leg_to_upper_ratio(bboxes):
    """
    다리 / 상체의 비율을 계산하고 결과를 반환하는 함수
    """
    leg_heights = []
    upper_body_height = None

    for bbox in bboxes:
        if bbox.get("label") == "다리":
            leg_heights.append(bbox["h"])
        elif bbox.get("label") == "상체":
            upper_body_height = bbox["h"]

    if len(leg_heights) == 2 and upper_body_height and upper_body_height > 0:
        avg_leg_height = sum(leg_heights) / 2
        ratio = avg_leg_height / upper_body_height
        if ratio > 1.30162008:
            return f"다리 / 상체 값은 {ratio:.4f}로 긴 편입니다."
        elif ratio < 0.9464469:
            return f"다리 / 상체 값은 {ratio:.4f}로 짧은 편입니다."
        else:
            return f"다리 / 상체 값은 {ratio:.4f}로 평균입니다."
    
    return "다리 또는 상체의 정보가 부족합니다."

def check_human_position(bboxes):
    """
    "사람전체" 레이블 중심 좌표의 위치를 판단하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == "사람전체":
            center_x = bbox["x"] + bbox["w"] / 2

            if center_x < 1280 / 3:
                return "객체가 좌측에 위치하고 있습니다."
            elif center_x > 1280 * 2 / 3:
                return "객체가 우측에 위치하고 있습니다."
            else:
                return "객체가 중앙에 위치하고 있습니다."

    return "사람전체 레이블이 존재하지 않습니다."

def check_label_existence(bboxes, label):
    """
    특정 레이블의 존재 여부를 확인하고 결과를 반환하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == label:
            return f"{label}(이)가 있습니다."
    return f"{label}가 없습니다."

def analyze_person(bboxes=None):
    """사람 그림의 모든 특징을 분석"""
    if bboxes is None:
        # JSON 파일에서 데이터 로드
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bboxes = data.get("annotations", {}).get("bbox", [])
    
    results = []
    results.append(check_human_position(bboxes))
    results.append(calculate_head_to_upper_ratio(bboxes))
    results.append(check_label_existence(bboxes, "머리"))
    results.append(check_label_existence(bboxes, "눈"))
    results.append(calculate_eye_to_face_ratio(bboxes))
    results.append(check_label_existence(bboxes, "코"))
    results.append(calculate_leg_to_upper_ratio(bboxes))
    return results

