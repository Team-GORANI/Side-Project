import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('annotation_database.db')
cursor = conn.cursor()

# 기존 테이블 삭제
cursor.executescript('''
    DROP TABLE IF EXISTS shape_descriptions;
    DROP TABLE IF EXISTS bounding_boxes;
    DROP TABLE IF EXISTS annotations;
    DROP TABLE IF EXISTS images_meta;
''')

# 새로운 테이블 생성
cursor.executescript('''
-- Meta 정보를 저장하는 테이블
CREATE TABLE images_meta (
    img_id VARCHAR(100) PRIMARY KEY,
    contributor VARCHAR(50),
    date_created DATE,
    img_path VARCHAR(255),
    label_path VARCHAR(255),
    img_size INTEGER,
    img_resolution VARCHAR(20),
    age INTEGER,
    sex VARCHAR(10)
);

-- Annotations 메인 정보를 저장하는 테이블
CREATE TABLE annotations (
    anno_id VARCHAR(100) PRIMARY KEY,
    img_id VARCHAR(100),
    class VARCHAR(50),
    bbox_count INTEGER,
    FOREIGN KEY (img_id) REFERENCES images_meta(img_id)
);

-- Bounding box 정보를 저장하는 테이블
CREATE TABLE bounding_boxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anno_id VARCHAR(100),
    label VARCHAR(50),
    x INTEGER,
    y INTEGER,
    w INTEGER,
    h INTEGER,
    FOREIGN KEY (anno_id) REFERENCES annotations(anno_id)
);

-- Shape description 정보를 저장하는 테이블
CREATE TABLE shape_descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anno_id VARCHAR(100),
    prop_obj_img TEXT,
    prop_obj_cls TEXT,
    prop_obj_face TEXT,
    num_obj TEXT,
    centroid_cls TEXT,
    FOREIGN KEY (anno_id) REFERENCES annotations(anno_id)
);
''')

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()

print("Database tables have been successfully created!")