## GPT로 이용해 간단하게 코드만든거 

import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, create_engine, JSON

from config import config


class DetectionResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    detections: List[dict] = Field(sa_column=JSON)  # JSON 필드로 탐지 결과 저장
    created_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat())  # ISO 형식 시간 저장


engine = create_engine(config.db_url)