import requests
import os
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    
    # 텔레그램 전송이 잘 됐는지 로그에 찍어보는 코드
    if res.status_code == 200:
        print("텔레그램 전송 성공!")
    else:
        print(f"텔레그램 전송 실패: {res.text}")

def run():
    now = datetime.now().strftime("%H:%M")
    
    # 주말 테스트용 가짜 데이터 메시지
    msg = f"🚀 *[{now}] 봇 연결 테스트 성공!*\n\n"
    msg += "주말이라 주식 시장이 닫혀있습니다.\n"
    msg += "월요일부터는 진짜 급등주를 잡아올게요! 🤖"
    
    send(msg)
