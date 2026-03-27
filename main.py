import os
import requests
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# 메시지 (일단 수동 분석 느낌으로 자동 생성)
today = datetime.now().strftime("%m/%d")

message = f"""
📊 {today} 미국 증시 요약

[미국 증시]
- S&P500: 혼조세
- 나스닥: 기술주 변동성 확대
- 주요 이유: 금리, AI 관련 기대감 혼재

[핵심 이슈]
1. (최중요) 금리 방향성 불확실성
2. (중요) AI 관련 빅테크 흐름
3. (참고) 반도체 수급 뉴스

[오늘 국장 전략]
- 유리한 섹터: 반도체, AI, 2차전지
- 피해야 할 구간: 갭상승 추격매수
- 매매 포인트: 눌림목 + 거래량 동반
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=data)
