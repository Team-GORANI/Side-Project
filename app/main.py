from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router  
import sys
import os

# 현재 디렉터리의 상위 디렉터리를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# CORS 미들웨어 설정
# 프론트엔드(localhost:5174)에서의 API 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('FRONTEND_URL', 'http://localhost:5173')], # 프론트엔드 서버 주소
    allow_credentials=True,                  # 자격 증명(쿠키 등) 허용
    allow_methods=["*"],                     # 모든 HTTP 메서드 허용
    allow_headers=["*"],                     # 모든 HTTP 헤더 허용
)

# temp 디렉토리가 없으면 생성
if not os.path.exists("temp"):
    os.makedirs("temp")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

# API 라우터 추가
app.include_router(router, prefix="/api")

# uvicorn 실행 코드 추가
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)