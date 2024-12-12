import json

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
            print(f"{a} / {b} 값은 {ratio:.4f}로 큰 편입니다.")
        elif ratio < reference_value[1]:
            print(f"{a} / {b} 값은 {ratio:.4f}로 작은 편입니다.")
        else:
            print(f"{a} / {b} 값은 {ratio:.4f}로 평균입니다.")
    else:
        print(f"{a} 또는 {b} 정보가 부족합니다.")

def check_house_position(bboxes):
    """
    "집전체" 레이블 중심 좌표의 위치를 판단하는 함수
    """
    for bbox in bboxes:
        if bbox.get("label") == "집전체":
            center_y = bbox["y"] + bbox["h"] / 2

            if center_y < 1280 / 3:
                print("객체가 하단에 위치하고 있습니다.")
            elif center_y > 1280 * 2 / 3:
                print("객체가 상단에 위치하고 있습니다.")
            else:
                print("객체가 중앙에 위치하고 있습니다.")
            return

    print("사람전체 레이블이 존재하지 않습니다.")

def check_label_existence(bboxes, label):
    """
    특정 레이블의 존재 여부를 확인하고 개수를 반환하는 함수
    """
    cnt = 0
    for bbox in bboxes:
        if bbox.get("label") == label:
            cnt+=1
    if cnt > 0:
        print(f"{label}(이)가 {cnt}개 있습니다.")
        return True
    print(f"{label}가 없습니다.")
    return False

# JSON 파일 경로
json_file_path = "C:/Users/Taehan/workspace/nbproject1/sideProject/code/Side-Project/data/meta/House/집_10_남_11951.json"  # 실제 파일 경로로 변경

# JSON 파일 열기
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 바운딩 박스 정보 가져오기
bboxes = data.get("annotations", {}).get("bbox", [])

# 함수 호출 및 결과 출력 예시
check_house_position(bboxes)
check_label_existence(bboxes, "집벽")
if check_label_existence(bboxes, "문"):
    calculate_a_to_b_ratio(bboxes, "문", "집벽")
if check_label_existence(bboxes, "지붕"):
    calculate_a_to_b_ratio(bboxes, "지붕", "집벽")
if check_label_existence(bboxes, "창문"):
    calculate_a_to_b_ratio(bboxes, "창문", "집벽")
if check_label_existence(bboxes, "연기"):
    calculate_a_to_b_ratio(bboxes, "연기", "집벽")

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
