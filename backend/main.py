from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from api import router
from config import Config

# Custom : Load functions from other files
from model.inference import infer_and_save

"""
# Event Handling
- FastAPI 서비스가 시작 또는 종료될 때 특정 함수를 호출하는 등의 행위
- Lifespan을 활용해 관리할 수 있다.
- 서비스가 시작될 때 호출되는 함수 -> yield -> 서비스가 종료될 때 호출되는 함수
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Step1. Handle input image


    # Step2. Load checkpoint
    logger.info("Loading model")

    # Input -> Select category
    infer_and_save(image, category) # model_path = ckpt

    yield # 비동기 구조(작업 끝날 때까지 기다림)

# Build FastAPI app
app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
