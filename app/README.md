# 사용 방법

---

## 1. 이미지 객체 탐지 결과 저장

이미지와 이미지 타입(예: 집, 나무, 사람)을 입력하여 객체 탐지 결과를 데이터베이스에 저장합니다. 

### 명령어

```bash
curl -X POST "http://127.0.0.1:8000/api/detect" \
-H "Content-Type: application/json" \
-d '{
  "image_type": "house",
  "image_path": "/data/house_test.png"
}'
```
### 파라미터 설명

image_type: 이미지 타입 (house, tree, person 중 하나).

image_path: 입력 이미지 파일 경로.

### 예제 응답

```json
{
  "status": "success",
  "image_path": "/data/house_test.png",
  "detections": [
    { "label": "문", "x": 57.80, "y": 120.53, "w": 27.01, "h": 38.27, "confidence": 0.93 },
    { "label": "지붕", "x": 40.97, "y": 54.82, "w": 161.71, "h": 63.17, "confidence": 0.91 },
    { "label": "집전체", "x": 37.30, "y": 27.80, "w": 163.85, "h": 130.62, "confidence": 0.85 },
    { "label": "굴뚝", "x": 11.06, "y": 16.93, "w": 81.60, "h": 82.17, "confidence": 0.79 },
    { "label": "집벽", "x": 40.39, "y": 106.14, "w": 160.64, "h": 52.67, "confidence": 0.77 },
    { "label": "연기", "x": 13.13, "y": 16.44, "w": 79.22, "h": 52.90, "confidence": 0.62 },
    { "label": "울타리", "x": 95.96, "y": 178.38, "w": 16.39, "h": 17.81, "confidence": 0.57 },
    { "label": "굴뚝", "x": 9.80, "y": 16.14, "w": 82.47, "h": 115.52, "confidence": 0.43 },
    { "label": "울타리", "x": 77.00, "y": 178.22, "w": 13.85, "h": 16.82, "confidence": 0.32 }
  ]
}
```
## 2. 심리 분석 요청

데이터베이스에 저장된 객체 탐지 결과를 바탕으로 크기, 위치 등의 정보를 판단하고, GPT를 통해 심리 분석 결과를 반환받습니다.

### 명령어

```bash
curl -X GET "http://127.0.0.1:8000/api/analysis/db에 저장되어 있는 이미지 경로"
```

### 파라미터 설명

image_path: 분석하고자 하는 이미지의 파일 경로.

### 예제 응답

```json
{
  "status": "success",
  "features_analyzed": [
    "BBox #1 (집전체) => (x=57, y=120, w=27, h=38) -> 크다",
    "BBox #2 (창문) => (x=40, y=54, w=161, h=63) -> 작다"
  ],
  "gpt_result": "집의 창문이 작고 전체적으로 큰 형태는 안정적인 환경을 추구하는 경향을 나타냅니다."
}
```
