import requests
import os
from datetime import datetime

# GitHub Secrets에서 값을 가져옵니다.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_market_data():
    # 야후 파이낸스 API 주소
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5EGSPC,%5EIXIC"
    
    # [중요] 브라우저처럼 보이기 위한 헤더 추가 (이게 없어서 에러가 났던 거예요!)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    res = requests.get(url, headers=headers).json()
    
    # 데이터가 잘 왔는지 확인
    if 'quoteResponse' not in res or not res['quoteResponse']['result']:
        raise Exception(f"데이터를 가져오지 못했습니다: {res}")

    sp500 = res['quoteResponse']['result'][0]['regularMarketChangePercent']
    nasdaq = res['quoteResponse']['result'][1]['regularMarketChangePercent']
    
    return sp500, nasdaq

def make_message():
    sp500, nasdaq = get_market_data()
    
    # 메시지 이모지 설정
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
