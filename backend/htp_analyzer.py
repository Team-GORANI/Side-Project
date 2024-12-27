import os
from fastapi import FastAPI, HTTPException, File, UploadFile, APIRouter
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

# Import from other files
# from tools.htp_analyzer import HTPAnalyzer
from tools.htp_anaylzer_ollama import HTPAnalyzer
from tools.house_func import analyze_house
from tools.tree_func import analyze_tree
from tools.person_func import analyze_person

"""
- GET : Load data, checkpoint from the server
- POST : CREATE과 같은 역할. Data를 등록한다.
- Pydantic - BaseModel : Dtype Validation

[To-do]
- [x] Save client's data using POST method
- [x] Type validation using pydantic-BaseModel
- [x] If image is not uploaded -> Except(error)
"""

router = APIRouter()

app = FastAPI(title="HTP 심리 분석 API")
htp_analyzer = HTPAnalyzer()

# Pydantic - Dtype validation
class HTPAnalysisRequest(BaseModel):
    drawing_type: str

# Validation : Tree, house, person 중에서 그린 그림인지 확인
ANALYSIS_FUNCTIONS = {
    'house': analyze_house,
    'tree': analyze_tree,
    'person': analyze_person
}

@app.post("/htp")
async def analyze_htp(
    drawing_type: str,
    file: UploadFile = File(...) # Required element
):
    """
    HTP 심리 분석 엔드포인트

    :param drawing_type: 분석할 그림 유형 ('house', 'tree', 'person')
    :param file: 업로드된 이미지 파일
    :return: GPT 기반 심리 분석 결과
    """

    # 이미지 저장 및 처리 (실제 구현에서는 임시 파일 처리 필요)
    contents = await file.read()

    try:
        # 특징 추출 함수 호출
        features = ANALYSIS_FUNCTIONS[drawing_type](contents)

        # GPT를 사용한 심리 분석
        analysis_result = htp_analyzer.analyze_with_gpt(features, drawing_type)

        return {
            "drawing_type": drawing_type,
            "analysis": analysis_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"분석 중 오류가 발생했습니다: {str(e)}"
        )

# Build FastAPI app
app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
