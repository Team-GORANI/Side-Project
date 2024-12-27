from pydantic import Field
from pydantic_settings import BaseSettings

from tools.house_func import analyze_house
from tools.tree_func import analyze_tree
from tools.person_func import analyze_person

"""
# Components
- db_url : Annotations(json) + Image
- model_path : Checkpoint file path (YOLO)

# Pydantic - BaseSetting
- default : 기본값
- env : 환경변수 이름
"""

# To-do : db_url setting (SQL?)
class Config(BaseSettings):
    model_path: str = Field(default="best_model.pth", env="MODEL_PATH")
    db_url: str = Field(default="To-do", env="DB_URL")

config = Config()

# Validation : Tree, house, person 중에서 그린 그림인지 확인
ANALYSIS_FUNCTIONS = {
    'house': analyze_house,
    'tree': analyze_tree,
    'person': analyze_person
}