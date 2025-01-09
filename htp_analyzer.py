import argparse

import requests

# Import from other files
from tools.house_func import analyze_house
from tools.person_func import analyze_person
from tools.tree_func import analyze_tree


class HTPAnalyzer:
    """HTP (House-Tree-Person) 심리 분석을 수행하는 클래스"""

    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def analyze_with_ollama(self, features, drawing_type):
        system_prompt = """You are a professional HTP psychologist and mental health counselor.
        Analyze both current psychological state and developmental influences through drawing features.
        Provide detailed analysis by connecting specific drawing features to psychological interpretations.
        - Use formal Korean (-습니다)
        - Do not use special characters
        - Avoid using personal pronouns or labels (e.g., 'you', 'artist', etc)
        - Only use emojis that are specifically defined in section headers
        """

        user_prompt = f"""
        === HTP Analysis Request ===
        Drawing Type: {drawing_type.upper()}
        Features Detected: {features}

        Using the bounding box coordinates [x,y,w,h], analyze the sketch and provide psychological interpretation in formal Korean.
        Translate all measurements into descriptive terms (e.g., centered, upper right, large, small):

        1. Personality Analysis:
        - Start with "1. 🔅 성격 특징 🔅"
        - Key personality traits
        - Analyze element sizes and placements from coordinates
        - Connect spatial features to personality traits
        - Interpret overall composition

        2. Social Characteristics:
        - Start with "2. 🌤️ 대인 관계 🌤️"
        - Family relationship patterns
        - Communication style
        - Interpret element spacing and relationship boundaries
        - Attachment patterns

        3. Current Mental State:
        - Start with "3. 🧘 현재 심리 상태 🧘"
        - Emotional stability
        - Developmental effects
        - Stress/anxiety levels
        - Coping mechanisms

        4. Mental Health Care:
        - Start with "4. 💪 멘탈 케어 Tips 💪"
        - Understanding past influences
        - Stress management suggestions
        - Provide practical suggestions
        - Growth potential
        """

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "mistral",  # 또는 다른 ollama 모델
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                },
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"분석 중 오류가 발생했습니다: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="HTP Psychological Analysis System")
    parser.add_argument(
        "type",
        choices=["house", "tree", "person"],
        help="Drawing type to analyze (house, tree, person)",
    )
    args = parser.parse_args()

    # Ollama 인스턴스 생성
    analyzer = HTPAnalyzer()

    # 그림 유형별 분석 함수 매핑
    analysis_functions = {
        "house": analyze_house,
        "tree": analyze_tree,
        "person": analyze_person,
    }

    # 선택된 그림 유형의 특징 분석
    features = analysis_functions[args.type]()

    # Ollama를 사용한 심리 분석
    analysis = analyzer.analyze_with_ollama(features, args.type)

    # 분석 결과 출력
    print(f"\n=== {args.type.upper()} Drawing Analysis ===")
    print(analysis)

    return analysis


if __name__ == "__main__":
    main()
