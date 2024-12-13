import json

# JSON 파일 경로 
json_file_path = "data/house_infomation.json"

def calculate_a_to_b_ratio(bboxes, a, b):
    """
    a / b의 비율을 계산하고 결과를 출력하는 함수
    """
    ## 각 기준 값
    if a == "지붕":
        reference_value = [0.923515, 0.665191]
    elif a == "창문":
        reference_value = [0.073576, 0.041115]
    elif a == "문":
        reference_value = [0.159336, 0.102952]
    elif a == "연기":
        reference_value = [0.187033, 0.069497]

    a_area = 0
    b_area = 0

    a_cnt = 0
    b_cnt = 0

    # 객체가 여러 개 있는 경우를 고려하여 area는 평균 값을 사용
    for bbox in bboxes:
        if bbox.get("label") == a:
            a_area += bbox["w"] * bbox["h"]
            a_cnt += 1
        elif bbox.get("label") == b:
            b_area += bbox["w"] * bbox["h"]
            b_cnt += 1

    if a_area != 0 and b_area != 0 and b_area > 0:
        ratio = (a_area/a_cnt) / (b_area/b_cnt)
        if ratio > reference_value[0]:
            return f"{a} / {b} 값은 {ratio:.4f}로 큰 편입니다."
        elif ratio < reference_value[1]:
            return f"{a} / {b} 값은 {ratio:.4f}로 작은 편입니다."
        else:
            return f"{a} / {b} 값은 {ratio:.4f}로 평균입니다."
    else:
        return f"{a} 또는 {b} 정보가 부족합니다."

def check_house_position(bboxes):
    """
    "집전체" 레이블 중심 좌표의 위치를 판단하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == "집전체":
            center_y = bbox["y"] + bbox["h"] / 2

            if center_y < 1280 / 3:
                return "객체가 하단에 위치하고 있습니다."
            elif center_y > 1280 * 2 / 3:
                return "객체가 상단에 위치하고 있습니다."
            else:
                return "객체가 중앙에 위치하고 있습니다."

    return "사람 전체 레이블이 존재하지 않습니다."

def check_label_existence(bboxes, label):
    """
    특정 레이블의 존재 여부를 확인하고 개수를 반환하는 함수
    """
    cnt = 0
    for bbox in bboxes:
        if bbox.get("label") == label:
            cnt+=1
    if cnt > 0:
        return f"{label}(이)가 {cnt}개 있습니다.", True
    return f"{label}가 없습니다.", False

def analyze_house(bboxes=None):
    """집 그림의 모든 특징을 분석"""
    if bboxes is None:
        # JSON 파일에서 데이터 로드
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bboxes = data.get("annotations", {}).get("bbox", [])
    
    results = []
    results.append(check_house_position(bboxes))
    label_exists, has_wall = check_label_existence(bboxes, "집벽")
    results.append(label_exists)
    
    for feature in ["문", "지붕", "창문", "연기"]:
        label_exists, exists = check_label_existence(bboxes, feature)
        if exists:
            results.append(calculate_a_to_b_ratio(bboxes, feature, "집벽"))
    return results


# Output:
# 객체가 하단에 위치하고 있습니다.
# 집벽(이)가 3개 있습니다.
# 문(이)가 1개 있습니다.
# 문 / 집벽 값은 0.3331로 큰 편입니다.
# 지붕(이)가 1개 있습니다.
# 지붕 / 집벽 값은 2.0160로 큰 편입니다.
# 창문(이)가 2개 있습니다.
# 창문 / 집벽 값은 0.1460로 큰 편입니다.
# 연기(이)가 1개 있습니다.
# 연기 / 집벽 값은 1.3622로 큰 편입니다.
