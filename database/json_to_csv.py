import json
from pathlib import Path
import pandas as pd
import os
import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description='Convert JSON files to DataFrame')
    parser.add_argument('--input_dir', required=True, help="Meta DB's path")

    return parser.parse_args()

def extract_bbox_info(file_path):
    """단일 JSON 파일에서 bbox 정보를 추출"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # bbox 정보 추출
    bbox_list = []
    for bbox in data['annotations']['bbox']:
        bbox_info = {
            'label': bbox['label'],
            'x': bbox['x'],
            'y': bbox['y'],
            'w': bbox['w'],
            'h': bbox['h'],
            'img_id': data['meta']['img_id']  # ID
        }
        bbox_list.append(bbox_info)

    return bbox_list

def process_all_files(directory_path):
    """모든 JSON 파일을 처리하여 하나의 데이터프레임으로 만듦"""
    all_bbox_info = []

    # 디렉토리 내의 모든 JSON 파일 처리
    for json_file in Path(directory_path).glob('*.json'):
        try:
            bbox_list = extract_bbox_info(json_file)
            all_bbox_info.extend(bbox_list)
            print(f"Successfully processed {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    # 데이터프레임 생성
    df = pd.DataFrame(all_bbox_info)

    return df

if __name__ == "__main__":
    args = arg_parse()

    # 현재 실행 경로에 파일을 저장하기 위한 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "meta_data.csv")

    # 데이터프레임 생성
    df = process_all_files(args.input_dir)

    # CSV 파일로 저장
    df.to_csv(output_file, index=False, encoding='utf-8')

    # 결과 출력
    print("\nProcessing completed!")
    print(f"Output file saved at: {output_file}")
    print(f"Total records: {len(df)}")
    print("\nLabel distribution:")
    print(df['label'].value_counts())
