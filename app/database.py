from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DetectionResult(Base):
    __tablename__ = "detection_results"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, unique=False, index=True)
    results = Column(JSON)  # bbox 데이터를 JSON 형식으로 저장

Base.metadata.create_all(bind=engine)

def save_to_database(image_path: str, results: dict):
    session = SessionLocal()
    try:
        # 1) 먼저 기존 레코드가 있는지 확인
        db_entry = session.query(DetectionResult).filter_by(image_path=image_path).first()
        if db_entry:
            # 2) 있으면 업데이트
            db_entry.results = results
        else:
            # 3) 없으면 새로 INSERT
            db_entry = DetectionResult(image_path=image_path, results=results)
            session.add(db_entry)
        session.commit()
    finally:
        session.close()