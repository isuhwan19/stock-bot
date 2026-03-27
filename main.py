import requests
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_market_data():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5EGSPC,%5EIXIC"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers).json()

    sp500 = res['quoteResponse']['result'][0]['regularMarketChangePercent']
    nasdaq = res['quoteResponse']['result'][1]['regularMarketChangePercent']

    return sp500, nasdaq

def make_message():
    sp500, nasdaq = get_market_data()

    msg = f"""
📊 미국 증시 요약 ({datetime.now().strftime('%m-%d')})

S&P500: {sp500:.2f}%
나스닥: {nasdaq:.2f}%

[핵심 해석]
"""

    if nasdaq >= 1:
        msg += "🔥 기술주 강세 → 반도체 / 2차전지 시초가 눌림 공략\n"
    elif nasdaq <= -1:
        msg += "⚠️ 기술주 약세 → 갭하락 후 반등만 단타\n"
    else:
        msg += "➖ 방향성 애매 → 테마주 단타 집중\n"

    msg += """
[국장 대응]
- 시초가 추격 금지
- 9:30~10:30 방향 확인
- 거래량 붙는 종목만 접근
"""

    return msg

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

if __name__ == "__main__":
    send_telegram(make_message())
