# JSON 파일 경로
json_file_path = "data/house_info.json"

# 한글 레이블을 영어로 매핑
label_mapping = {
    "집전체": "house_whole",
    "지붕": "roof",
    "집벽": "wall",
    "문": "door",
    "창문": "window",
    "굴뚝": "chimney",
    "연기": "smoke",
    "울타리": "fence",
    "길": "road",
    "연못": "pond",
    "산": "mountain",
    "나무": "tree",
    "꽃": "flower",
    "잔디": "grass",
    "태양": "sun",
}


def check_label_existence(bboxes, label):
    """
    Check the existence of a specific label and return a message and count.
    """
    cnt = sum(1 for bbox in bboxes if bbox.get("label") == label)
    eng_label = label_mapping.get(label, label)
    return (
        f"There are {cnt} '{eng_label}' objects."
        if cnt > 0
        else f"No '{eng_label}' found."
    ), cnt


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
        large_str = "Large roof: a tendency to daydream and flee to superficial interpersonal relationships"
        small_str = "Small roof: a lack of psychological protection, realistic thinking"
    elif label_type == "창문":  # window
        large_threshold = 0.073576
        small_threshold = 0.041115
        large_str = "Large window: inflated self-esteem, grandiose self"
        small_str = "Small window: a psychological distancing, shy personality"
    elif label_type == "문":  # door
        large_threshold = 0.159336
        small_threshold = 0.102952
        large_str = "Large door: a dependent person, a desire for active social contact"
        small_str = "Small door: reluctance, helplessness to come into contact with the environment"
    elif label_type == "연기":  # smoke
        large_threshold = 0.187033
        small_threshold = 0.069497
        large_str = "Large smoke: a lack of home warmth"
        small_str = "Small smoke: suppression of emotional expression"
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
                return "Top position: idealistic and fanciful"
            elif center_y > 1280 * 2 / 3:
                return "Bottom position: Realistic, Unstable Sentiment"
            else:
                return "Center position: A stable home environment, reflecting the sense of reality"

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


def analyze_house(bboxes):
    """집 그림의 모든 특징을 분석"""
    results = []

    # 바운딩박스 정보 -> 문자열로 변환
    bbox_info = []
    for bbox in bboxes:
        eng_label = label_mapping.get(bbox["label"], bbox["label"])
        bbox_info.append(
            f"{eng_label}: [{bbox['x']},{bbox['y']},{bbox['w']},{bbox['h']}]"
        )

    results.append(", ".join(bbox_info))
    results.append("")

    # 집의 위치 분석
    results.append(check_house_position(bboxes))
    canopy_msg, canopy_area = analyze_canopy(bboxes)
    results.append(canopy_msg)

    # 비율 파악해야 하는 것들
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
                results.append("Road existence: Welcome to Social Interrelationships")
            if feature == "잔디":
                results.append("Grass existence: psychological stability")
            if feature == "울타리":
                results.append(
                    "Fence existence: trying to build a psychological bulwark"
                )

    return results
