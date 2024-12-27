import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

from config import config

""" [To-do]
- [] Create DB using SQL method
"""
# Type validation


# Using config(DB path), Create SQL DB
engine = create_engine(config.db_url)
