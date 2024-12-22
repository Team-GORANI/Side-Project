import json
import sqlite3
from pathlib import Path
import datetime
import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description='Process JSON files and insert data into SQLite database.')
    parser.add_argument('--input_dir', type=str, default='./data/meta/집', help='Meta data path')
    parser.add_argument('--db_path', type=str, default='./database.db', help='Path to the SQLite database file.')
    return parser.parse_args()

def create_database(db_path):
    """데이터베이스 생성 및 스키마 설정"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Meta 정보를 저장하는 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images_meta (
            img_id VARCHAR(100) PRIMARY KEY,
            contributor VARCHAR(50),
            date_created DATE,
            img_path VARCHAR(255),
            label_path VARCHAR(255),
            img_size INTEGER,
            img_resolution VARCHAR(20),
            age INTEGER,
            sex VARCHAR(10)
        )
    ''')

    # Annotations 메인 정보를 저장하는 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotations (
            anno_id VARCHAR(100) PRIMARY KEY,
            img_id VARCHAR(100),
            class VARCHAR(50),
            bbox_count INTEGER,
            FOREIGN KEY (img_id) REFERENCES images_meta(img_id)
        )
    ''')

    # Bounding box 정보를 저장하는 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bounding_boxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anno_id VARCHAR(100),
            label VARCHAR(50),
            x INTEGER,
            y INTEGER,
            w INTEGER,
            h INTEGER,
            FOREIGN KEY (anno_id) REFERENCES annotations(anno_id)
        )
    ''')

    # Shape description 정보를 저장하는 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shape_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anno_id VARCHAR(100),
            prop_obj_img TEXT,
            prop_obj_cls TEXT,
            prop_obj_face TEXT,
            num_obj TEXT,
            centroid_cls TEXT,
            FOREIGN KEY (anno_id) REFERENCES annotations(anno_id)
        )
    ''')

    conn.commit()
    return conn

def process_file(file_path, conn):
    """단일 JSON 파일을 처리하여 데이터베이스에 저장"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Meta 데이터 삽입
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO images_meta (
            img_id, contributor, date_created, img_path,
            label_path, img_size, img_resolution, age, sex
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['meta']['img_id'],
        data['meta']['contributor'],
        data['meta']['date_created'],
        data['meta']['img_path'],
        data['meta']['label_path'],
        data['meta']['img_size'],
        data['meta']['img_resolution'],
        data['meta']['age'],
        data['meta']['sex']
    ))

    # Annotations 데이터 삽입
    cursor.execute("""
        INSERT OR REPLACE INTO annotations (
            anno_id, img_id, class, bbox_count
        ) VALUES (?, ?, ?, ?)
    """, (
        data['annotations']['anno_id'],
        data['meta']['img_id'],
        data['annotations']['class'],
        data['annotations']['bbox_count']
    ))

    # Bounding boxes 데이터 삽입
    for bbox in data['annotations']['bbox']:
        cursor.execute("""
            INSERT INTO bounding_boxes (
                anno_id, label, x, y, w, h
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['annotations']['anno_id'],
            bbox['label'],
            bbox['x'],
            bbox['y'],
            bbox['w'],
            bbox['h']
        ))

    # Shape descriptions 데이터 삽입
    cursor.execute("""
        INSERT OR REPLACE INTO shape_descriptions (
            anno_id, prop_obj_img, prop_obj_cls, prop_obj_face,
            num_obj, centroid_cls
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data['annotations']['anno_id'],
        json.dumps(data['shape_description']['prop_obj_img']),
        json.dumps(data['shape_description']['prop_obj_cls']),
        json.dumps(data['shape_description']['prop_obj_face']),
        json.dumps(data['shape_description']['num_obj']),
        json.dumps(data['shape_description']['centroid_cls'])
    ))

    conn.commit()

def process_all_files(directory_path, db_path):
    """모든 JSON 파일을 처리"""
    conn = create_database(db_path)

    for json_file in Path(directory_path).glob('*.json'):
        try:
            process_file(json_file, conn)
            print(f"Successfully processed {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    conn.close()


if __name__ == "__main__":
    args = arg_parse()
    process_all_files(args.input_dir, args.db_path)
