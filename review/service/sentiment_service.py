import requests
import os

AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://localhost:8001/analyze/")


def analyze_sentiment(texts):
    """
    FastAPI 컨테이너에 감성 분석 요청을 보냄
    """
    results = []
    for text in texts:
        payload = {"text": text}
        headers = {"Content-Type": "application/json"}
        response = requests.post(AI_SERVER_URL, json=payload, headers=headers)

        if response.status_code == 200:
            results.append(response.json())
        else:
            print(f"🚨 FastAPI 응답 오류! 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")
            results.append({"PosNeg": 1, "Confidence": 0})  # 기본값 반환

    return results
