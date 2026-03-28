from datetime import datetime
import requests
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def run():
    now = datetime.now().strftime("%H:%M")
    
    # 테스트용 데이터
    stocks = [
        {"name": "테스트종목A", "change": 4.2},
        {"name": "테스트종목B", "change": 2.1},
    ]

    for stock in stocks:
        if stock["change"] > 3:
            send(f"🔥 [{now}] 급등 감지\n{stock['name']} +{stock['change']}%")
