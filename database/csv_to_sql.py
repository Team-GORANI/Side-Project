import pandas as pd
import sqlite3
import os
import argparse

def create_database(db_path):
    """데이터베이스 생성 및 테이블 스키마 설정"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 기존 테이블이 있다면 삭제
    cursor.execute('DROP TABLE IF EXISTS bbox_data')

    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE bbox_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            w INTEGER NOT NULL,
            h INTEGER NOT NULL,
            img_id TEXT NOT NULL
        )
    ''')

    conn.commit()
    return conn

def csv_to_sql(csv_path, db_path):
    """CSV 파일을 읽어서 SQL 데이터베이스로 변환"""
    # CSV 파일 읽기
    df = pd.read_csv(csv_path)

    # 데이터베이스 생성
    conn = create_database(db_path)

    # DataFrame을 SQL 테이블로 변환
    df.to_sql('bbox_data', conn, if_exists='replace', index=False)

    # 변환 결과 확인
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bbox_data")
    total_records = cursor.fetchone()[0]

    cursor.execute("SELECT label, COUNT(*) as count FROM bbox_data GROUP BY label")
    label_distribution = cursor.fetchall()

    conn.close()

    return total_records, label_distribution

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV to SQLite database')
    parser.add_argument('--csv_name', default='meta_data.csv',
                      help='Input CSV file name (default: bbox_data.csv)')
    parser.add_argument('--db_name', default='women_meta.db',
                      help='Output database file name (default: bbox_database.db)')

    args = parser.parse_args()

    # 현재 디렉토리 경로 가져오기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, args.csv_name)
    db_path = os.path.join(current_dir, args.db_name)

    # CSV가 존재하는지 확인
    if not os.path.exists(csv_path):
        print(f"Error: CSV file '{csv_path}' not found!")
        exit(1)

    # 변환 실행
    try:
        total_records, label_distribution = csv_to_sql(csv_path, db_path)

        print("\nConversion completed successfully!")
        print(f"Database saved at: {db_path}")
        print(f"\nTotal records: {total_records}")
        print("\nLabel distribution:")
        for label, count in label_distribution:
            print(f"{label}: {count}")

    except Exception as e:
        print(f"Error during conversion: {e}")
