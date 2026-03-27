import requests
import os
import yfinance as yf
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_market_analysis():
    # 1. 수집할 데이터 심볼 (S&P500, 나스닥, 변동성지수, 10년물 금리, 원/달러 환율)
    symbols = {
        "S&P500": "^GSPC",
        "Nasdaq": "^IXIC",
        "VIX(공포지수)": "^VIX",
        "US10Y(금리)": "^TNX",
        "USD/KRW": "KRW=X"
    }
    
    results = {}
    for name, sym in symbols.items():
        ticker = yf.Ticker(sym)
        hist = ticker.history(period="2d")
        if len(hist) < 2: continue
        
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        change = ((current - prev) / prev) * 100
        results[name] = {"val": current, "chg": change}

    return results

def analyze_strategy(data):
    # 데이터 기반 로직 분석
    nasdaq_chg = data['Nasdaq']['chg']
    vix_val = data['VIX(공포지수)']['val']
    exchange_chg = data['USD/KRW']['chg']
    
    strategy = ""
    if nasdaq_chg > 1.0 and exchange_chg < 0:
        strategy = "🚀 [상승장] 외인 수급 기대! 반도체 대형주 공격적 접근"
    elif nasdaq_chg < -1.0 or vix_val > 20:
        strategy = "⚠️ [위험] 리스크 관리 우선. 현금 비중 확대 및 방어주 위주"
    else:
        strategy = "⚖️ [혼조] 지수보다는 개별 테마주(AI, 바이오) 순환매 대응"
        
    return strategy

def send_pro_report():
    data = get_market_analysis()
    strategy = analyze_strategy(data)
    today = datetime.now().strftime("%m/%d")
    
    msg = f"""
📅 **{today} 미 증시 마감 & 국장 전략**

**[주요 지수]**
- S&P500: {data['S&P500']['val']:.0f} ({data['S&P500']['chg']:+.2f}%)
- 나스닥: {data['Nasdaq']['val']:.0f} ({data['Nasdaq']['chg']:+.2f}%)
- VIX지수: {data['VIX(공포지수)']['val']:.2f} ({data['VIX(공포지수)']['chg']:+.2f}%)

**[매크로 환경]**
- 미 10년물 금리: {data['US10Y(금리)']['val']:.2f}%
- 원/달러 환율: {data['USD/KRW']['val']:.1f}원 ({data['USD/KRW']['chg']:+.2f}%)

**[오늘의 투자 전략]**
{strategy}

*매수 포인트: {"나스닥 강세로 인한 반도체 소부장" if data['Nasdaq']['chg'] > 0 else "지수 방어용 배당주 및 저PBR"}*
"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    try:
        send_pro_report()
        print("전략 리포트 전송 완료!")
    except Exception as e:
        print(f"에러 발생: {e}")
