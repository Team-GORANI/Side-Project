import json
import argparse
from openai import OpenAI
from house_func import analyze_house, json_file_path
from tree_func import analyze_tree, json_file_path
from person_func import analyze_person, json_file_path

class HTPAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze_with_gpt(self, features, drawing_type):
        """GPT API를 사용하여 분석 결과를 얻는 메서드"""
        prompts = {
            "house": """
                다음은 HTP 심리검사에서 집 그림의 특징입니다:
                {features}
                특징을 참고해서 심리를 분석해주세요.
            """,
            "tree": """
                다음은 HTP 심리검사에서 나무 그림의 특징입니다:
                {features}
                특징을 참고해서 심리를 분석해주세요.
            """,
            "person": """
                다음은 HTP 심리검사에서 사람 그림의 특징입니다:
                {features}         
                특징을 참고해서 심리를 분석해주세요.
            """
        }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", #gpt-4
                messages=[
                    {"role": "system", "content": "당신은 HTP 심리검사 전문가입니다."},
                    {"role": "user", "content": prompts[drawing_type].format(features=' '.join(features))}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"분석 중 오류가 발생했습니다: {str(e)}"

def main():
    # 파서 설정
    parser = argparse.ArgumentParser(description='HTP 심리검사 분석기')
    parser.add_argument('type', choices=['person', 'house', 'tree'],
                      help='분석할 그림 유형 (person, house, tree)')
    args = parser.parse_args()
    
    # API 키 설정
    API_KEY ="API Key 설정"
    analyzer = HTPAnalyzer(API_KEY)
    
    analysis_functions = {
        'person': analyze_person,
        'house': analyze_house,
        'tree': analyze_tree
    }
    
    results = {}
    
    features = analysis_functions[args.type]()
    analysis = analyzer.analyze_with_gpt(features, args.type)
    results[args.type] = analysis

    print(f"\n=== {args.type.upper()} 그림 분석 결과 ===")
    print(analysis)
    
    return results

if __name__ == "__main__":
    main()
