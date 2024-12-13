import json

# JSON 파일 경로 
json_file_path = "data/tree_infomation.json"

def check_label_existence(bboxes, label):
    """
    특정 레이블의 존재 여부를 확인하고 개수를 반환하며 결과를 출력하는 함수
    """
    cnt = 0
    for bbox in bboxes:
        if bbox.get("label") == label:
            cnt += 1
    if cnt > 0:
        return f"{label}(이)가 {cnt}개 있습니다.", cnt
    else:
        return f"{label}가 없습니다.", 0

def get_area_of_label(bboxes, label):
    """
    특정 라벨이 있는 첫 번째 객체의 면적을 반환 (수관은 하나라고 가정)
    """
    for bbox in bboxes:
        if bbox.get("label") == label:
            w = bbox.get("w", 0)
            h = bbox.get("h", 0)
            return w * h
    return 0

def get_areas_of_label(bboxes, label):
    """
    특정 라벨의 모든 객체 면적 리스트를 반환
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
    canopy_area 대비 areas에 있는 객체들의 비율을 계산하고,
    주어진 기준에 따라 크다/작다를 판정하는 함수
    
    label_type에 '기둥' 또는 '가지'를 전달.
    """
    if label_type == "기둥":
        large_threshold = 0.650350
        small_threshold = 0.381995
    elif label_type == "가지":
        large_threshold = 0.145762
        small_threshold = 0.359546
    else:
        return

    for area in areas:
        ratio = area / canopy_area
        if ratio >= large_threshold:
            return f'{label_type}/수관 비율이 {ratio:.6f} 이므로 {label_type}가 크다'
        elif ratio <= small_threshold:
            return f'{label_type}/수관 비율이 {ratio:.6f} 이므로 {label_type}가 작다'

def check_animal_in_pillar(bboxes):
    """
    '다람쥐', '새' 라벨의 객체 중앙점이 기둥 내부에 있는지 판별하는 함수
    """
    # 기둥 찾기
    pillar_box = None
    for bbox in bboxes:
        if bbox.get("label") == "기둥":
            pillar_box = bbox
            break

    if pillar_box is None:
        return "기둥이 없습니다."

    px, py = pillar_box["x"], pillar_box["y"]
    pw, ph = pillar_box["w"], pillar_box["h"]

    animal_found = False
    for bbox in bboxes:
        label = bbox.get("label", "")
        if label in ["다람쥐", "새"]:
            cx = bbox["x"] + bbox["w"] / 2
            cy = bbox["y"] + bbox["h"] / 2
            
            if px <= cx <= px + pw and py <= cy <= py + ph:
                animal_found = True
                break

    if animal_found:
        return "동물이 나무에 존재한다"
    else:
        return "동물이 나무에 존재하지 않는다"

def check_tree_position(bboxes):
    """
    "나무전체" 레이블 중심 좌표의 위치를 판단하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == "나무전체":
            center_y = bbox["y"] + bbox["h"] / 2
            # 해상도가 1280x1280이라고 가정
            if center_y < 1280 / 3:
                return "나무전체가 하단에 위치하고 있습니다."
            elif center_y > 1280 * 2 / 3:
                return "나무전체가 상단에 위치하고 있습니다."
            else:
                return "나무전체가 중앙에 위치하고 있습니다."
    return "나무전체 레이블이 존재하지 않습니다."

def analyze_canopy(bboxes):
    """
    수관 존재 여부를 확인하고 관련 분석을 수행하는 함수
    """
    # 수관 존재 확인
    canopy_msg, canopy_exists = check_label_existence(bboxes, "수관")
    
    if not canopy_exists:
        return "해당 JSON 파일에 수관(label='수관')이 존재하지 않습니다.", 0
    
    # 수관 면적 구하기
    canopy_area = get_area_of_label(bboxes, "수관")
    return canopy_msg, canopy_area

def analyze_tree(bboxes=None):
    """나무의 모든 특징을 분석"""
    if bboxes is None:
        # JSON 파일에서 데이터 로드
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bboxes = data.get("annotations", {}).get("bbox", [])
    
    results = []
    results.append(check_tree_position(bboxes))
    
    # 수관 분석
    canopy_msg, canopy_area = analyze_canopy(bboxes)
    results.append(canopy_msg)
    
    if canopy_area > 0:  # 수관이 있을 때만 추가 분석
        # 기둥 분석
        pillar_msg, pillar_exists = check_label_existence(bboxes, "기둥")
        results.append(pillar_msg)
        if pillar_exists:
            pillar_areas = get_areas_of_label(bboxes, "기둥")
            ratio_result = check_and_print_ratio(canopy_area, pillar_areas, "기둥")
            if ratio_result:
                results.append(ratio_result)
        
        # 가지 분석
        branch_msg, branch_exists = check_label_existence(bboxes, "가지")
        results.append(branch_msg)
        if branch_exists:
            branch_areas = get_areas_of_label(bboxes, "가지")
            ratio_result = check_and_print_ratio(canopy_area, branch_areas, "가지")
            if ratio_result:
                results.append(ratio_result)
    
    return results

# output
# 나무전체가 중앙에 위치하고 있습니다.
# 수관(이)가 1개 있습니다.
# 기둥(이)가 1개 있습니다.
# 기둥/수관 비율이 0.311793 이므로 기둥가 작다
# 가지(이)가 1개 있습니다.
# 가지/수관 비율이 0.579989 이므로 가지가 크다
# 다람쥐(이)가 1개 있습니다.
# 새(이)가 1개 있습니다.
# 동물이 나무에 존재하지 않는다
