import json

# JSON 파일 경로 
json_file_path = "data/house_information.json"

def check_label_existence(bboxes, label):
    """
    Check the existence of a specific label and return a message and count.
    """
    cnt = sum(1 for bbox in bboxes if bbox.get("label") == label)
    return (f"There are {cnt} '{label}' objects." if cnt > 0 else f"No '{label}' found."), cnt

def get_area_of_label(bboxes, label):
    """
    Returns the area of the first object with the given label.
    Assume only one canopy if label='집벽'.
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
    if label_type == "지붕":  # roof
        large_threshold = 0.923515
        small_threshold = 0.665191
        large_str = "This roof is large"
        small_str = "This roof is small"
    elif label_type == "창문":  # window
        large_threshold = 0.073576
        small_threshold = 0.041115
        large_str = "This window is large"
        small_str = "This window is small"
    elif label_type == "문":  # door
        large_threshold = 0.159336
        small_threshold = 0.102952
        large_str = "This door is large"
        small_str = "This door is small"
    elif label_type == "연기":  # smoke
        large_threshold = 0.187033
        small_threshold = 0.069497
        large_str = "This smoke is large"
        small_str = "This smoke is small"
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

def check_house_position(bboxes):
    """
    "집전체" 레이블 중심 좌표의 위치를 판단하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == "집전체":
            center_y = bbox["y"] + bbox["h"] / 2

            if center_y < 1280 / 3:
                return "The house is located at the top."
            elif center_y > 1280 * 2 / 3:
                return "The house is located at the bottom."
            else:
                return "The house is located at the center."

    return "No 'house' label found."

def analyze_canopy(bboxes):
    """
    Check the existence of canopy and return its area.
    """
    canopy_msg, canopy_exists = check_label_existence(bboxes, "집벽")
    if canopy_exists == 0:
        return canopy_msg, 0
    canopy_area = get_area_of_label(bboxes, "집벽")
    return canopy_msg, canopy_area

def analyze_house(bboxes=None):
    """집 그림의 모든 특징을 분석"""
    if bboxes is None:
        # JSON 파일에서 데이터 로드
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bboxes = data.get("annotations", {}).get("bbox", [])
    
    results = []
    results.append(check_house_position(bboxes))
    canopy_msg, canopy_area = analyze_canopy(bboxes)
    results.append(canopy_msg)
    
    # 비율 파악해야하는 것들
    for feature in ["문", "지붕", "창문", "연기"]:
        label_msg, exists = check_label_existence(bboxes, feature)
        results.append(label_msg)
        if exists:
            label_areas = get_areas_of_label(bboxes, feature)
            ratio_result = check_and_print_ratio(canopy_area, label_areas, feature)
            if ratio_result:
                results.append(ratio_result)
    
    # 존재 유무만 파악
    for feature in ["길", "잔디", "울타리"]:
        label_msg, exists = check_label_existence(bboxes, feature)
        if exists:
            if feature == "길":
                results.append(f"There is road")
            if feature == "잔디":
                results.append(f"There is grass")
            if feature == "울타리":
                results.append(f"There is fence")
            

    # Interpretations mapping
    # If a certain keyword is found in `results`, add the corresponding interpretation in English.
    interpretations = {
        "top": "Top position: idealistic and fanciful",
        "center": "Center position: A stable home environment, reflecting the sense of reality",
        "bottom": "Bottom position: Realistic, Unstable Sentiment",
        "This roof is large": "Large roof: a tendency to daydream and flee to superficial interpersonal relationships",
        "This roof is small": "Small roof: a lack of psychological protection, realistic thinking",
        "This window is large": "Large window: inflated self-esteem, grandiose self",
        "This window is small": "Small window: a psychological distancing, shy personality",
        "This door is large": "Large door: a dependent person, a desire for active social contact",
        "This door is small": "Small door: reluctance, helplessness and indecision to come into contact with the environment",
        "This smoke is large": "Large smoke: a lack of home warmth",
        "This smoke is small": "Small smoke: suppression of emotional expression",
        "There is road": "Road existence: Welcome to Social Interrelationships",
        "There is grass": "Grass existence: psychological stability",
        "There is fence": "Fence existence: trying to build a psychological bulwark"
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
        keys_list = list(interpretations.keys())
        # Check key_list
        if res in keys_list:
            final_interpretation.append(interpretations[res])

    return final_interpretation

# final_interpretation:
# ['Top position: idealistic and fanciful', 
#  'Large door: a dependent person, a desire for active social contact', 
#  'Large roof: a tendency to daydream and flee to superficial interpersonal relationships', 
#  'Large window: inflated self-esteem, grandiose self', 
#  'Large smoke: a lack of home warmth', 
#  'Road existence: Welcome to Social Interrelationships', 
#  'Grass existence: psychological stability', 
#  'Fence existence: trying to build a psychological bulwark']
