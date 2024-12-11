import streamlit as st
import json
import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

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

def load_image_and_annotations(img_path, json_path):
    """
    이미지와 JSON 파일에서 annotation 정보를 로드합니다.

    Args:
        img_path (str): 이미지 파일 경로
        json_path (str): JSON 파일 경로

    Returns:
        tuple: 이미지 배열, bbox 정보 리스트
    """
    # 이미지 로드
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # JSON 파일 로드
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Bounding boxes 추출
    bboxes = data['annotations']['bbox']

    return image, bboxes

def draw_bboxes(image, bboxes):
    """
    이미지에 bounding boxes를 그립니다.

    Args:
        image (numpy.ndarray): 원본 이미지
        bboxes (list): bounding boxes 정보 리스트

    Returns:
        numpy.ndarray: bbox가 그려진 이미지
    """
    # 이미지 복사
    annotated_image = image.copy()

    # 다양한 색상 팔레트
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255)   # Cyan
    ]

    # 각 bbox 그리기
    for i, bbox in enumerate(bboxes):
        x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
        label = bbox['label']

        # 색상 순환
        color = colors[i % len(colors)]

        # 사각형 그리기
        cv2.rectangle(
            annotated_image,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        # 레이블 텍스트 추가
        cv2.putText(
            annotated_image,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )

    return annotated_image

def main():
    st.title('🖼️ Image Annotation Visualization')

    # 소스 디렉토리 설정 (현재 스크립트 위치 기준 상대 경로)
    project_root = os.path.expanduser('~/Desktop/Git/Side-Project/data')
    source_dir = os.path.join(project_root, '원천데이터', '집')
    meta_dir = os.path.join(project_root, 'meta', '집')

    # 파일 목록 가져오기
    image_files = [f for f in os.listdir(source_dir) if f.endswith('.jpg')]

    # 파일 선택
    selected_image = st.selectbox('이미지를 선택하세요:', image_files)

    # 전체 경로 구성
    img_path = os.path.join(source_dir, selected_image)
    json_path = os.path.join(meta_dir, selected_image.replace('.jpg', '.json'))

    # 이미지와 bbox 로드
    try:
        image, bboxes = load_image_and_annotations(img_path, json_path)

        # bbox 그리기
        annotated_image = draw_bboxes(image, bboxes)

        # Streamlit에 이미지 표시
        st.image(annotated_image, caption=f'Annotated Image: {selected_image}')

        # 추가 정보 표시
        st.subheader('Annotation Details')
        for bbox in bboxes:
            st.write(f"Label: {bbox['label']}, Position: (x:{bbox['x']}, y:{bbox['y']}), Size: {bbox['w']}x{bbox['h']}")

    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.error("이미지나 JSON 파일을 로드하는 데 문제가 있습니다.")

if __name__ == '__main__':
    main()
