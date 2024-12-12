import json

def check_label_existence(bboxes, label):
    """
    특정 레이블의 존재 여부를 확인하고 개수를 반환하며 결과를 출력하는 함수
    """
    cnt = 0
    for bbox in bboxes:
        if bbox.get("label") == label:
            cnt += 1
    if cnt > 0:
        print(f"{label}(이)가 {cnt}개 있습니다.")
    else:
        print(f"{label}가 없습니다.")
    return cnt

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
            print(f'{label_type}/수관 비율이 {ratio:.6f} 이므로 {label_type}가 크다')
        elif ratio <= small_threshold:
            print(f'{label_type}/수관 비율이 {ratio:.6f} 이므로 {label_type}가 작다')

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
        print("기둥이 없습니다.")
        return

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
        print("동물이 나무에 존재한다")
    else:
        print("동물이 나무에 존재하지 않는다")

def check_tree_position(bboxes):
    """
    "나무전체" 레이블 중심 좌표의 위치를 판단하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == "나무전체":
            center_y = bbox["y"] + bbox["h"] / 2
            # 해상도가 1280x1280이라고 가정
            if center_y < 1280 / 3:
                print("나무전체가 하단에 위치하고 있습니다.")
            elif center_y > 1280 * 2 / 3:
                print("나무전체가 상단에 위치하고 있습니다.")
            else:
                print("나무전체가 중앙에 위치하고 있습니다.")
            return
    print("나무전체 레이블이 존재하지 않습니다.")

# 메인 로직
# 특정 JSON 파일 경로 설정
json_file = "data/tree_infomation.json"

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

bboxes = data.get("annotations", {}).get("bbox", [])

# 나무전체 위치 확인
check_tree_position(bboxes)

# 수관 존재 확인
if check_label_existence(bboxes, "수관") == 0:
    print("해당 JSON 파일에 수관(label='수관')이 존재하지 않습니다.")
else:
    # 수관 면적 구하기
    canopy_area = get_area_of_label(bboxes, "수관")

    # 기둥 존재 확인
    check_label_existence(bboxes, "기둥")
    # 기둥 면적들
    column_areas = get_areas_of_label(bboxes, "기둥")
    if len(column_areas) > 0:
        # 기둥 비율 체크
        check_and_print_ratio(canopy_area, column_areas, "기둥")

    # 가지 존재 확인
    check_label_existence(bboxes, "가지")
    # 가지 면적들
    branch_areas = get_areas_of_label(bboxes, "가지")
    if len(branch_areas) > 0:
        # 가지 비율 체크
        check_and_print_ratio(canopy_area, branch_areas, "가지")

    # 동물("다람쥐", "새") 존재 확인
    check_label_existence(bboxes, "다람쥐")
    check_label_existence(bboxes, "새")
    # 동물 체크
    check_animal_in_pillar(bboxes)


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
