import os, random
from collections import defaultdict
from enum import Enum
from typing import Tuple, List

import numpy as np
from PIL import Image


# 지원되는 이미지 확장자 리스트
IMG_EXTENSIONS = [
    ".jpg", ".JPG", ".jpeg", ".JPEG",
    ".png", ".PNG", ".ppm",
    ".PPM", ".bmp", ".BMP",
]


def is_image_file(filename):
    """
    - 파일 이름이 이미지 확장자를 가지는지 확인하는 함수
    - bool : If extension is Image
    """
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)