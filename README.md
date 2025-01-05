# Team-GORANI : Side Project

나무, 집, 사람 중에서 원하는 대상을 자유롭게 그려보세요. 우리는 여러분의 그림을 활용해서 HTP 심리상담 서비스를 제공합니다.

## 🧐 How to use??

1. 그림을 그리고 싶은 대상을 선택해주세요. (나무, 사람, 집)

<img width="400" alt="image" src="https://github.com/Team-GORANI/Side-Project/tree/main/src/sample_main_menu.png">

3. 여러분의 창의력을 활용해서 자유롭게 그림을 그려주세요! 또는 사진을 업로드할 수도 있습니다.

<img width="400" alt="image" src="https://github.com/Team-GORANI/Side-Project/tree/main/src/sample_tree.png">

5. 모두 그렸다면 "분석결과 보러가기"를 누르고, 심리 상담 결과를 확인해보세요.


``` mermaid
graph LR
    subgraph Docker["Docker Compose"]
        subgraph FE["React"]
            React["React App]
        end

        subgraph BE["FastAPI"]
            FastAPI["FastAPI Server"]
            Models["ML Models"]
        end

        React -->|HTTP Requests| FastAPI
        FastAPI -->|JSON Response| React
        FastAPI -->|Inference| Models
    end

    style Docker fill:#e7f7ff,stroke:#333
    style FE fill:#f9f9f9,stroke:#666
    style BE fill:#f9f9f9,stroke:#666
```

## ✨ Features
- Full-stack app : React, FastAPI, SQL, GCP
- 이미지를 분석하고, 이를 활용한 심리 상담 결과를 제공합니다. 심리 상담에는 GPT가 사용됩니다.

## ➕ Prerequisites
- Python 3.9 or higher
- Back-end : fastapi, uvicorn
- Model : ultralytics
- DB : sqlalchemy
- LLM : openai

## 🚩 How to use?

``` bash
git clone https://github.com/Team-GORANI/Side-Project.git
cd Side-Project

docker-compose up --build
```