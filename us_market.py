import requests
import os
import yfinance as yf
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_fear_and_greed():
    try:
        url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers)
        data = res.json()
        
        score = int(data['fear_and_greed']['score'])
        rating_raw = data['fear_and_greed']['rating'].lower()
        
        if "extreme fear" in rating_raw:
            rating_kr = "극도의 공포 🥶"
        elif "fear" in rating_raw:
            rating_kr = "공포 😨"
        elif "neutral" in rating_raw:
            rating_kr = "중립 😐"
        elif "extreme greed" in rating_raw:
            rating_kr = "극도의 탐욕 🤑"
        else:
            rating_kr = "탐욕 😏"
            
        return f"{score}점 ({rating_kr})"
    except Exception as e:
        return "데이터 확인 불가 ⚠️"

def get_top_news():
    try:
        url = "https://news.google.com/rss/search?q=미국+증시&hl=ko&gl=KR&ceid=KR:ko"
        res = requests.get(url)
        root = ET.fromstring(res.text)
        
        headlines = ""
        for i, item in enumerate(root.findall('.//item')[:3]):
            title = item.find('title').text
            title = title.replace('[', '(').replace(']', ')').replace('*', '').replace('_', '')
            headlines += f"{i+1}. {title}\n"
            
        return headlines if headlines else "최신 뉴스가 없습니다."
    except Exception as e:
        return f"뉴스를 불러오지 못했습니다. ({e})"

def get_market_analysis():
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
        if len(hist) < 2: 
            results[name] = {"val": 0, "chg": 0}
            continue
        
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        change = ((current - prev) / prev) * 100
        results[name] = {"val": current, "chg": change}

    return results

def analyze_strategy(data):
    nasdaq_chg = data['Nasdaq']['chg']
    vix_val = data['VIX(공포지수)']['val']
    exchange_chg = data['USD/KRW']['chg']
    
    if nasdaq_chg > 1.0 and exchange_chg < 0:
        strategy = "🚀 [상승장] 외인 수급 기대! 반도체 대형주 공격적 접근"
    elif nasdaq_chg < -1.0 or vix_val > 20:
        strategy = "⚠️ [위험] 리스크 관리 우선. 현금 비중 확대 및 방어주 위주"
    else:
        strategy = "⚖️ [혼조] 지수보다는 개별 테마주 순환매 대응"
        
    return strategy

def send_pro_report():
    data = get_market_analysis()
    strategy = analyze_strategy(data)
    fg_index = get_fear_and_greed()
    news_text = get_top_news()
    
    # 한국 시간 기준으로 날짜 설정
    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST).strftime("%m/%d")
    
    msg = f"""
📅 **{today} 미 증시 마감 & 국장 전략**

**[주요 지수]**
- S&P500: {data['S&P500']['val']:.0f} ({data['S&P500']['chg']:+.2f}%)
- 나스닥: {data['Nasdaq']['val']:.0f} ({data['Nasdaq']['chg']:+.2f}%)
- VIX지수: {data['VIX(공포지수)']['val']:.2f}
- Fear & Greed: {fg_index}

**[매크로 환경]**
- 미 10년물 금리: {data['US10Y(금리)']['val']:.2f}%
- 원/달러 환율: {data['USD/KRW']['val']:.1f}원 ({data['USD/KRW']['chg']:+.2f}%)

**[🔥 간밤의 핵심 뉴스 Top 3]**
{news_text}
**[오늘의 투자 전략]**
{strategy}
"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # parse_mode="Markdown"을 추가하여 글자를 굵게 만듭니다.
    requests.post(url, data={
        "chat_id": CHAT_ID, 
        "text": msg,
        "parse_mode": "Markdown"
    })

def run():
    try:
        send_pro_report()
        print("미국 증시 리포트 전송 완료!")
    except Exception as e:
        print(f"us_market 실행 중 에러 발생: {e}")
