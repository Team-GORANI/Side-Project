import streamlit as st
import json, os, cv2
import numpy as np
import argparse
from PIL import ImageFont, ImageDraw, Image

def parse_args():
    """ [Required file tree structure]
data/
│
├── 원천데이터/
│   └── 집/
│       ├── 집_7_남_00060.jpg
│       ├── 집_7_남_00061.jpg
│       └── ... (기타 이미지 파일들)
│
├── meta/ # 이름 변경 가능합니다.
│   └── 집/
│       ├── 집_7_남_00060.json
│       ├── 집_7_남_00061.json
│       └── ... (해당 JSON 파일들)
│
└── scripts/
    └── bbox_visualization.py
    """
    parser = argparse.ArgumentParser(description='Train dataset Visusalization')
    parser.add_argument('--data_dir', type=str, default='/home/ng-youn/Desktop/Git/Side-Project/data',
                    help='Train data가 있는 경로')
    parser.add_argument('--category', type=str, default="집",
                        help="집, 나무, 남자사람, 여자사람 중에서 선택해주세요.")

    return parser.parse_args()

def load_image_and_annotations(img_path, json_path):
    """
    이미지와 JSON 파일에서 annotation 정보를 로드합니다.

    Args:
        img_path (str): 이미지 파일 경로
        json_path (str): JSON 파일 경로

    Returns:
        tuple: 이미지 배열, bbox 정보 리스트
    """
    try:
        # 이미지 로드
        image = cv2.imread(img_path)
        if image is None:
            raise ValueError(f"이미지를 로드할 수 없습니다: {img_path}")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # JSON 파일 로드
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Bounding boxes 추출
        bboxes = data['annotations']['bbox']

        return image, bboxes

    except json.JSONDecodeError:
        raise ValueError(f"JSON 파일을 파싱할 수 없습니다: {json_path}")
    except FileNotFoundError:
        raise ValueError(f"파일을 찾을 수 없습니다: {json_path}")

def find_korean_font():
    possible_paths = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # 대체 폰트
        "/usr/share/fonts/opentype/nanum/NanumGothic.ttf"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None

def draw_bboxes_with_pil(image, bboxes):
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # 색상 팔레트
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255)   # Cyan
    ]

    # 한글 폰트 로드
    font_path = find_korean_font()

    if font_path is None:
        st.warning("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, 20)

    # 각 bbox 그리기
    for i, bbox in enumerate(bboxes):
        x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
        label = bbox['label']

        # 색상 순환
        color = colors[i % len(colors)]

        # 사각형 그리기
        draw.rectangle([x, y, x+w, y+h], outline=color, width=2)

        # 레이블 텍스트 추가
        draw.text((x, y-25), label, font=font, fill=color)

    return np.array(pil_image)

def main():
    args = parse_args()
    st.title('🖼️ Image Annotation Visualization')

    # 소스 디렉토리 설정
    source_dir = os.path.join(args.data_dir, '원천데이터', args.category)
    meta_dir = os.path.join(args.data_dir, 'meta', args.category)

    # 파일 목록 가져오기
    image_files = [f for f in os.listdir(source_dir) if f.endswith('.jpg')]

    # 파일 선택
    selected_image = st.selectbox('이미지를 선택하세요:', image_files)

    # 전체 경로 구성
    img_path = os.path.join(source_dir, selected_image)
    json_path = os.path.join(meta_dir, selected_image.replace('.jpg', '.json'))

    image, bboxes = load_image_and_annotations(img_path, json_path)

    # bbox 그리기 (PIL 사용)
    annotated_image = draw_bboxes_with_pil(image, bboxes)

    # Streamlit에 이미지 표시
    st.image(annotated_image, caption=f'Annotated Image: {selected_image}')

    # 추가 정보 표시
    st.subheader('Annotation Details')
    for bbox in bboxes:
        st.write(f"Label: {bbox['label']}, Position: (x:{bbox['x']}, y:{bbox['y']}), Size: {bbox['w']}x{bbox['h']}")

if __name__ == '__main__':
    main()
