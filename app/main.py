from fastapi import FastAPI
import sys
import os

# 현재 디렉터리의 상위 디렉터리를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import router  # 수정 후 경로

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HTP 심리 검사 서버가 실행 중입니다."}

# API 라우터 추가
app.include_router(router, prefix="/api")

# uvicorn 실행 코드 추가
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)