import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    print(f"메시지 전송 시도... (ID: {CHAT_ID})")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    print(f"결과: {res.status_code}, {res.text}")

def run():
    print("surge_stock.run() 시작")
    # 무조건 테스트용 데이터를 만들어서 보냅니다.
    msg = "🚀 봇 연결 테스트 성공! 주말에도 잘 작동합니다."
    send(msg)

if __name__ == "__main__":
    run()
