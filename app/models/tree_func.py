
# JSON 파일 경로 
json_file_path = "data/tree_info.json"

# 한글 레이블을 영어로 매핑
label_mapping = {
    "나무전체": "tree_whole",
    "기둥": "trunk",
    "수관": "crown",
    "가지": "branch",
    "뿌리": "root",
    "나뭇잎": "leaf",
    "꽃": "flower",
    "열매": "fruit",
    "그네": "swing",
    "새": "bird",
    "다람쥐": "squirrel",
    "구름": "cloud",
    "달": "moon",
    "별": "star"
}

def check_label_existence(bboxes, label):
    """
    Check the existence of a specific label and return a message and count.
    """
    cnt = sum(1 for bbox in bboxes if bbox.get("label") == label)
    eng_label = label_mapping.get(label, label) 
    return (f"There are {cnt} '{eng_label}' objects." if cnt > 0 else f"No '{eng_label}' found."), cnt

def get_area_of_label(bboxes, label):
    """
    Returns the area of the first object with the given label.
    Assume only one canopy if label='수관'.
    """
    for bbox in bboxes:
        if bbox.get("label") == label:
            w = bbox.get("w", 0)
            h = bbox.get("h", 0)
            return w * h
    return 0

def get_areas_of_label(bboxes, label):
    """
    Returns a list of areas for all objects with the given label.
    """
    areas = []
    for bbox in bboxes:
        if bbox.get("label") == label:
            w = bbox.get("w", 0)
            h = bbox.get("h", 0)
            areas.append(w * h)
    return areas

def check_and_print_ratio(canopy_area, areas, label_type):
    """
    Compare object areas (trunk or branch) with the canopy area
    and determine if it's large or small based on thresholds.
    """
    if label_type == "기둥":  # trunk
        large_threshold = 0.650350
        small_threshold = 0.381995
        large_str = "Large trunk: actively engaged, creative environment"
        small_str = "Small trunk: helplessness, maladaptation"
    elif label_type == "가지":  # branch
        large_threshold = 0.145762
        small_threshold = 0.359546
        large_str = "Large branch: inflated self-esteem, grandiose self"
        small_str = "Small branch: weakness and incompetence"
    else:
        return None

    for area in areas:
        ratio = area / canopy_area
        if ratio >= large_threshold:
            return large_str
        elif ratio <= small_threshold:
            return small_str
    # If not large or small, we do not print anything special
    return None

def check_animal_in_pillar(bboxes):
    """
    Check if an animal ('다람쥐', '새') is inside the pillar area.
    """
    pillar_box = None
    for bbox in bboxes:
        if bbox.get("label") == "기둥":
            pillar_box = bbox
            break

    if pillar_box is None:
        return "No pillar found."

    px, py = pillar_box["x"], pillar_box["y"]
    pw, ph = pillar_box["w"], pillar_box["h"]

    for bbox in bboxes:
        label = bbox.get("label", "")
        if label in ["다람쥐", "새"]:
            cx = bbox["x"] + bbox["w"] / 2
            cy = bbox["y"] + bbox["h"] / 2
            if px <= cx <= px + pw and py <= cy <= py + ph:
                return "Animal inside the hole: identification with animals, attachment-related, seeking stability, symbol of the womb"
    return "No animal inside the tree."

def check_tree_position(bboxes):
    """
    Determine the vertical position of the '나무전체' (whole tree).
    Returns a string describing if it's top, center, or bottom.
    """
    for bbox in bboxes:
        if bbox.get("label") == "나무전체":
            center_y = bbox["y"] + bbox["h"] / 2
            if center_y < 1280 / 3:
                return "Top position: goal-oriented tendency"
            elif center_y > 1280 * 2 / 3:
                return "Bottom position: self-protective attitude"
            else:
                return "Center position: inner stability, growth desire"
    return "No 'whole tree' label found."

def analyze_canopy(bboxes):
    """
    Check the existence of canopy and return its area.
    """
    canopy_msg, canopy_exists = check_label_existence(bboxes, "수관")
    if canopy_exists == 0:
        return canopy_msg, 0
    canopy_area = get_area_of_label(bboxes, "수관")
    return canopy_msg, canopy_area

def analyze_tree(bboxes):
    """나무 그림의 모든 특징을 분석"""
    results = []

    # 바운딩박스 정보 -> 문자열로 변환
    bbox_info = []
    for bbox in bboxes:
        eng_label = label_mapping.get(bbox['label'], bbox['label'])
        bbox_info.append(f"{eng_label}: [{bbox['x']},{bbox['y']},{bbox['w']},{bbox['h']}]")
    
    results.append(", ".join(bbox_info))
    results.append("")

    results.append(check_tree_position(bboxes))        # tree position
    canopy_msg, canopy_area = analyze_canopy(bboxes)
    results.append(canopy_msg)                         # canopy info
    
    if canopy_area > 0:
        # Column
        pillar_msg, pillar_exists = check_label_existence(bboxes, "기둥")
        results.append(pillar_msg)
        if pillar_exists:
            pillar_areas = get_areas_of_label(bboxes, "기둥")
            ratio_result = check_and_print_ratio(canopy_area, pillar_areas, "기둥")
            if ratio_result:
                results.append(ratio_result)

        # Branch
        branch_msg, branch_exists = check_label_existence(bboxes, "가지")
        results.append(branch_msg)
        if branch_exists:
            branch_areas = get_areas_of_label(bboxes, "가지")
            ratio_result = check_and_print_ratio(canopy_area, branch_areas, "가지")
            if ratio_result:
                results.append(ratio_result)

        # Animal in pillar
        animal_result = check_animal_in_pillar(bboxes)
        results.append(animal_result)

    return results

# Example run
# final_result = analyze_tree()
# print("\n".join(final_result))

# output 
# Bottom position: self-protective attitude
# Large column: actively engaged, creative environment
# Large branch: inflated self-esteem, grandiose self
# Animal inside the hole: identification with animals, attachment-related, seeking stability, symbol of the womb