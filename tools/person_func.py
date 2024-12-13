import json

# JSON 파일 경로 
json_file_path = "data/person_info.json"

# 한글 레이블을 영어로 매핑
label_mapping = {
    "사람전체": "person_whole",
    "머리": "head",
    "얼굴": "face",
    "눈": "eye",
    "코": "nose",
    "입": "mouth",
    "귀": "ear",
    "머리카락": "hair",
    "목": "neck",
    "상체": "upper_body",
    "팔": "arm",
    "손": "hand",
    "다리": "leg",
    "발": "foot",
    "단추": "button",
    "주머니": "pocket",
    "운동화": "sneakers",
    "남자구두": "dress_shoes"
}

def calculate_head_to_upper_ratio(bboxes):
    """
    Calculate the head-to-upper body ratio and print the result in English.
    """
    head_area = None
    upper_body_area = None

    for bbox in bboxes:
        if bbox.get("label") == "머리":
            head_area = bbox["w"] * bbox["h"]
        elif bbox.get("label") == "상체":
            upper_body_area = bbox["w"] * bbox["h"]

        if head_area is not None and upper_body_area is not None:
            break

    if head_area is not None and upper_body_area is not None and upper_body_area > 0:
        ratio = head_area / upper_body_area
        if ratio > 2.2925420:
            return "Large head: Intellectual curiosity, lack of physical energy."
        elif ratio < 1.2819802:
            return "No head: Neurosis, depression, autistic tendencies."

def calculate_eye_to_face_ratio(bboxes):
    """
    Calculate the eye-to-face ratio and print the result in English.
    """
    eye_areas = []
    face_area = None

    for bbox in bboxes:
        if bbox.get("label") == "눈":
            eye_areas.append(bbox["w"] * bbox["h"])
        elif bbox.get("label") == "얼굴":
            face_area = bbox["w"] * bbox["h"]

        if len(eye_areas) == 2 and face_area is not None:
            break

    if len(eye_areas) == 2 and face_area is not None and face_area > 0:
        avg_eye_area = sum(eye_areas) / 2
        ratio = avg_eye_area / face_area
        if ratio > 0.0427861542:
            return "Large eyes: Suspicion of others, hypersensitivity."
        elif ratio < 0.0221859051:
            return "No eyes: Guilt feelings."

def calculate_leg_to_upper_ratio(bboxes):
    """
    Calculate the leg-to-upper body ratio and print the result in English.
    """
    leg_heights = []
    upper_body_height = None

    for bbox in bboxes:
        if bbox.get("label") == "다리":
            leg_heights.append(bbox["h"])
        elif bbox.get("label") == "상체":
            upper_body_height = bbox["h"]

        if len(leg_heights) == 2 and upper_body_height is not None:
            break

    if len(leg_heights) == 2 and upper_body_height is not None and upper_body_height > 0:
        avg_leg_height = sum(leg_heights) / 2
        ratio = avg_leg_height / upper_body_height
        if ratio > 1.30162008:
            return "Long legs: Desire for stability and independence."
        elif ratio < 0.9464469:
            return "Short legs: Loss of independence, tendency for dependency."

def check_human_position(bboxes):
    """
    Check the position of the "entire person" label and print the result in English.
    """
    for bbox in bboxes:
        if bbox.get("label") == "사람전체":
            center_x = bbox["x"] + bbox["w"] / 2

            if center_x < 1280 / 3:
                return "Left position: Obsession with the past, introverted tendencies."
            elif center_x > 1280 * 2 / 3:
                return "Right position: Future-oriented attitude, extroverted tendencies."
            else:
                return "Center position: Self-centeredness, confidence in interpersonal relationships."

def check_label_existence(bboxes, label):
    """
    Check if a specific label exists and print the result in English.
    """
    for bbox in bboxes:
        if bbox.get("label") == label:
            return  # Nothing is printed if the label exists

def analyze_person(bboxes=None):
    """사람 그림의 모든 특징을 분석"""
    if bboxes is None:
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                meta = data.get("meta", {})
                bboxes = data.get("annotations", {}).get("bbox", [])
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return []

    results = []
    
    # 이미지 해상도
    results.append(f"Image Resolution: {meta.get('img_resolution')}")
    
    # 바운딩박스 형식 설명
    results.append("\nBoxes type = [x,y,w,h]")
    
    # 바운딩박스 정보 -> 문자열로 변환
    bbox_info = []
    for bbox in bboxes:
        eng_label = label_mapping.get(bbox['label'], bbox['label'])
        bbox_info.append(f"{eng_label}: [{bbox['x']},{bbox['y']},{bbox['w']},{bbox['h']}]")
    
    results.append(", ".join(bbox_info))
    results.append("")

    # Call functions
    analysis_results = [
        check_human_position(bboxes),
        calculate_head_to_upper_ratio(bboxes),
        check_label_existence(bboxes, "머리"),
        check_label_existence(bboxes, "눈"),
        calculate_eye_to_face_ratio(bboxes),
        check_label_existence(bboxes, "코"),
        calculate_leg_to_upper_ratio(bboxes)
    ]
    
    for result in analysis_results:
        if result is not None:
            results.append(result)

    return results

# Example run
# final_result = analyze_person()
# print("\n".join(final_result))