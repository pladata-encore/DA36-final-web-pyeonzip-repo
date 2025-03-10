import requests
import os

# ✅ FastAPI 서버 URL 설정 (환경 변수 or 기본값)
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://localhost:8001/extract_keywords_hf/")

def extract_keywords(text):
    """
    FastAPI 컨테이너에 키워드 추출 요청을 보냄
    """
    payload = {"review": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(AI_SERVER_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"🚨 FastAPI 응답 오류! 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        return {"keybert_keywords": [], "top_sim_tags": []}  # 빈값 반환
