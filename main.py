import requests
import os
import yfinance as yf
from datetime import datetime

# GitHub Secrets에서 값을 가져옵니다.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_market_data():
    # yfinance를 사용하여 데이터를 가져옵니다 (차단 우회)
    tickers = yf.Tickers('^GSPC ^IXIC')
    
    # S&P 500 데이터
    sp500_data = tickers.tickers['^GSPC'].history(period="2d")
    sp500_change = ((sp500_data['Close'].iloc[-1] - sp500_data['Close'].iloc[-2]) / sp500_data['Close'].iloc[-2]) * 100
    
    # 나스닥 데이터
    nasdaq_data = tickers.tickers['^IXIC'].history(period="2d")
    nasdaq_change = ((nasdaq_data['Close'].iloc[-1] - nasdaq_data['Close'].iloc[-2]) / nasdaq_data['Close'].iloc[-2]) * 100
    
    return sp500_change, nasdaq_change

def make_message():
    sp500, nasdaq = get_market_data()
    
    s_icon = "🔥" if sp500 > 0 else "📉"
    n_icon = "🔥" if nasdaq > 0 else "📉"
    
    msg = f"""
📊 **미국 증시 요약 ({datetime.now().strftime('%m-%d')})**

S&P500: {sp500:.2f}% {s_icon}
나스닥: {nasdaq:.2f}% {n_icon}

[핵심 해석]
{"🚀 기술주 강세! 반도체/2차전지 주목" if nasdaq >= 1 else "⚠️ 기술주 약세, 보수적 대응 필요"}
"""
    return msg

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    res = requests.post(url, data=payload)
    return res.json()

if __name__ == "__main__":
    try:
        message = make_message()
        send_telegram(message)
        print("메시지 전송 완료!")
    except Exception as e:
        print(f"에러 발생: {e}")
