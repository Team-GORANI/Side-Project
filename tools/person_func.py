import json

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
            print("Large head: Intellectual curiosity, lack of physical energy.")
        elif ratio < 1.2819802:
            print("No head: Neurosis, depression, autistic tendencies.")

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
            print("Large eyes: Suspicion of others, hypersensitivity.")
        elif ratio < 0.0221859051:
            print("No eyes: Guilt feelings.")

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
            print("Long legs: Desire for stability and independence.")
        elif ratio < 0.9464469:
            print("Short legs: Loss of independence, tendency for dependency.")

def check_human_position(bboxes):
    """
    Check the position of the "entire person" label and print the result in English.
    """
    for bbox in bboxes:
        if bbox.get("label") == "사람전체":
            center_x = bbox["x"] + bbox["w"] / 2

            if center_x < 1280 / 3:
                print("Left position: Obsession with the past, introverted tendencies.")
            elif center_x > 1280 * 2 / 3:
                print("Right position: Future-oriented attitude, extroverted tendencies.")
            else:
                print("Center position: Self-centeredness, confidence in interpersonal relationships.")
            return

def check_label_existence(bboxes, label):
    """
    Check if a specific label exists and print the result in English.
    """
    for bbox in bboxes:
        if bbox.get("label") == label:
            return  # Nothing is printed if the label exists

# JSON file path
json_file_path = "C:/Users/Windows/Desktop/Side_Project/data/person/label/남자사람_10_남_02666.json"  # Update to actual file path

# Open the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get bounding box information
bboxes = data.get("annotations", {}).get("bbox", [])

# Call functions and print results
check_human_position(bboxes)
calculate_head_to_upper_ratio(bboxes)
check_label_existence(bboxes, "머리")
check_label_existence(bboxes, "눈")
calculate_eye_to_face_ratio(bboxes)
check_label_existence(bboxes, "코")
calculate_leg_to_upper_ratio(bboxes)