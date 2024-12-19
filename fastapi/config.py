## GPT로 이용해 간단하게 코드만든거 

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Database or application-specific settings
    db_url: str = Field(default="sqlite:///./db.sqlite3", env="DB_URL")
    
    # YOLOv8 model-related settings
    model_path: str = Field(default="yolov8n.pt", env="MODEL_PATH")
    data_path: str = Field(default="data.yaml", env="DATA_PATH")  # Data configuration file
    num_classes: int = Field(default=10, env="NUM_CLASSES")  # Number of detection classes
    # => 집, 나무, 사람 각각 모델, datapath, numclass등을 따로 선언해야할듯


    image_size: int = Field(default=640, env="IMAGE_SIZE")  # Image size for inference
    conf_threshold: float = Field(default=0.25, env="CONF_THRESHOLD")  # Confidence threshold
    iou_threshold: float = Field(default=0.45, env="IOU_THRESHOLD")  # IoU threshold for NMS

    # Training-related settings => 필요하려나
    epochs: int = Field(default=100, env="EPOCHS")  # Number of training epochs
    batch_size: int = Field(default=16, env="BATCH_SIZE")  # Batch size for training
    learning_rate: float = Field(default=0.001, env="LEARNING_RATE")  # Learning rate

    # Device settings
    device: str = Field(default="cpu", env="DEVICE")  # Device to use ('cuda' or 'cpu')


config = Config()