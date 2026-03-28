import requests
from bs4 import BeautifulSoup
import os
import yfinance as yf
from datetime import datetime, timezone, timedelta

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def get_technical_indicators(code, market_type):
    """시장 타입(.KS 또는 .KQ)에 맞춰 기술적 지표를 계산합니다."""
    try:
        # 코스피면 .KS, 코스닥이면 .KQ를 붙입니다.
        suffix = ".KS" if market_type == "KOSPI" else ".KQ"
        ticker = yf.Ticker(f"{code}{suffix}")
        df = ticker.history(period="1mo")

        if len(df) < 20: return "측정불가", "측정불가"

        # RSI 계산
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # 추세 (정배열: 종가 > 5일선 > 20일선)
        ma5 = df['Close'].rolling(window=5).mean().iloc[-1]
        ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
        is_bull = "✅ 정배열" if df['Close'].iloc[-1] > ma5 > ma20 else "➖ 혼조"

        rsi_status = f"{current_rsi:.1f} (과열🔥)" if current_rsi >= 70 else f"{current_rsi:.1f} (보통)"
        return rsi_status, is_bull
    except:
        return "조회실패", "조회실패"

def get_investor_data(code):
    """수급 데이터 조회"""
    try:
        url = f"https://finance.naver.com/item/frgn.naver?code={code}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.find('table', {'class': 'type2'}).find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 9:
                inst = cols[5].get_text(strip=True).replace(',', '')
                fore = cols[6].get_text(strip=True).replace(',', '')
                inst_txt = "🔴 매수" if int(inst) > 0 else "🔵 매도" if int(inst) < 0 else "보합"
                fore_txt = "🔴 매수" if int(fore) > 0 else "🔵 매도" if int(fore) < 0 else "보합"
                return inst_txt, fore_txt
        return "정보없음", "정보없음"
    except: return "실패", "실패"

def get_market_candidates(sosok_code, market_name):
    """특정 시장(코스피/코스닥)의 상승 후보군을 가져옵니다."""
    url = f"https://finance.naver.com/sise/sise_rise.naver?sosok={sosok_code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.find('table', {'class': 'type_2'}).find_all('tr')
    
    results = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 10: continue
        try:
            a_tag = cols[1].find('a')
            if not a_tag: continue
            code = a_tag['href'].split('code=')[1]
            change_pct = float(cols[4].get_text(strip=True).replace('%', '').strip())
            volume = int(cols[5].get_text(strip=True).replace(',', ''))
            
            # 필터: 7~20% 상승 & 거래량 50만주 이상
            if 7.0 <= change_pct <= 20.0 and volume >= 500000:
                results.append({
                    "name": a_tag.get_text(strip=True),
                    "code": code,
                    "price": cols[2].get_text(strip=True),
                    "change": change_pct,
                    "vol": volume,
                    "market": market_name
                })
        except: continue
    return results

def run():
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    if now.weekday() >= 5:
        send(f"🛌 *[{now.strftime('%H:%M')}] 주말 휴장*\n봇도 함께 쉽니다.")
        return

    # 1. 코스피(0)와 코스닥(1) 모두 긁어오기
    print("시장 데이터 수집 중...")
    all_stocks = get_market_candidates(0, "KOSPI") + get_market_candidates(1, "KOSDAQ")
    
    if not all_stocks:
        send("⚠️ 조건에 맞는 종목이 없습니다.")
        return

    # 2. 통합된 종목 중 거래량 상위 5개 추출
    top_stocks = sorted(all_stocks, key=lambda x: x['vol'], reverse=True)[:5]
    
    for s in top_stocks:
        s['inst'], s['fore'] = get_investor_data(s['code'])
        s['rsi'], s['trend'] = get_technical_indicators(s['code'], s['market'])

    msg = f"🏛️ *[{now.strftime('%H:%M')}] 전시장 통합 분석*\n"
    msg += "_코스피+코스닥 거래량 Top 5_\n\n"
    
    for i, s in enumerate(top_stocks):
        market_label = "🏢" if s['market'] == "KOSPI" else "🚀"
        msg += f"{i+1}. *{s['name']}* ({s['code']}) {market_label}\n"
        msg += f"📈 등락: +{s['change']}% | {s['price']}원\n"
        msg += f"📊 수급: 외인({s['fore']}) / 기관({s['inst']})\n"
        msg += f"🌡️ RSI: {s['rsi']} | {s['trend']}\n\n"
        
    msg += "💡 *Market Tip*: 🏢는 코스피, 🚀는 코스닥 종목입니다."
    send(msg)
