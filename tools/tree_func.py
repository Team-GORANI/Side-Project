import json

# JSON 파일 경로 
json_file_path = "data/tree_information.json"

def check_label_existence(bboxes, label):
    """
    Check the existence of a specific label and return a message and count.
    """
    cnt = sum(1 for bbox in bboxes if bbox.get("label") == label)
    return (f"There are {cnt} '{label}' objects." if cnt > 0 else f"No '{label}' found."), cnt

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
    Compare object areas (column or branch) with the canopy area
    and determine if it's large or small based on thresholds.
    """
    if label_type == "기둥":  # column
        large_threshold = 0.650350
        small_threshold = 0.381995
        large_str = "This column is large"
        small_str = "This column is small"
    elif label_type == "가지":  # branch
        large_threshold = 0.145762
        small_threshold = 0.359546
        large_str = "This branch is large"
        small_str = "This branch is small"
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
                return "There is an animal inside the tree."
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
                return "The whole tree is located at the top."
            elif center_y > 1280 * 2 / 3:
                return "The whole tree is located at the bottom."
            else:
                return "The whole tree is located at the center."
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

def analyze_tree(bboxes=None):
    """Analyze the tree and return interpretations."""
    if bboxes is None:
        # Load from JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bboxes = data.get("annotations", {}).get("bbox", [])

    results = []
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

        # Squirrel
        squirrel_msg, _ = check_label_existence(bboxes, "다람쥐")
        results.append(squirrel_msg)

        # Bird
        bird_msg, _ = check_label_existence(bboxes, "새")
        results.append(bird_msg)

        # Animal in pillar
        animal_result = check_animal_in_pillar(bboxes)
        results.append(animal_result)

    # Interpretations mapping
    # If a certain keyword is found in `results`, add the corresponding interpretation in English.
    interpretations = {
        "top": "Top position: goal-oriented tendency",
        "center": "Center position: inner stability, growth desire",
        "bottom": "Bottom position: self-protective attitude",
        "This column is large": "Large column: actively engaged, creative environment",
        "This column is small": "Small column: helplessness, maladaptation",
        "This branch is large": "Large branch: inflated self-esteem, grandiose self",
        "This branch is small": "Small branch: weakness and incompetence",
        "There is an animal inside the tree.": "Animal inside the hole: identification with animals, attachment-related, seeking stability, symbol of the womb"
    }

    final_interpretation = []

    for res in results:
        # Check position keywords
        if "top" in res.lower():
            final_interpretation.append(interpretations["top"])
        elif "center" in res.lower():
            final_interpretation.append(interpretations["center"])
        elif "bottom" in res.lower():
            final_interpretation.append(interpretations["bottom"])
        
        # Check column/branch/animal lines
        for key in ["This column is large", "This column is small", 
                    "This branch is large", "This branch is small", 
                    "There is an animal inside the tree."]:
            if key in res:
                final_interpretation.append(interpretations[key])

    return final_interpretation

# Example run
# final_result = analyze_tree()
# print("\n".join(final_result))

# output 
# Bottom position: self-protective attitude
# Large column: actively engaged, creative environment
# Large branch: inflated self-esteem, grandiose self
# Animal inside the hole: identification with animals, attachment-related, seeking stability, symbol of the womb