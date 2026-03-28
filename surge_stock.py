import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def get_closing_candidates():
    # 코스닥 상승 종목 페이지 (sosok=1)
    url = "https://finance.naver.com/sise/sise_rise.naver?sosok=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    table = soup.find('table', {'class': 'type_2'})
    rows = table.find_all('tr')
    
    candidates = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 10: continue
        
        try:
            name = cols[1].get_text(strip=True)
            current_price = cols[2].get_text(strip=True)
            change_pct = float(cols[4].get_text(strip=True).replace('%', '').strip())
            volume = int(cols[5].get_text(strip=True).replace(',', ''))
            
            # 🔥 [종가매매 필터링 조건]
            # 1. 상승률이 7% ~ 20% 사이 (너무 높으면 내일 갭 하락 위험, 낮으면 힘이 없음)
            # 2. 거래량이 최소 50만 주 이상 (유동성 확보)
            if 7.0 <= change_pct <= 20.0 and volume >= 500000:
                candidates.append({
                    "name": name,
                    "price": current_price,
                    "change": change_pct,
                    "volume": format(volume, ',')
                })
        except (ValueError, IndexError):
            continue
            
    # 거래량 순으로 정렬하여 상위 5개만 반환
    candidates = sorted(candidates, key=lambda x: int(x['volume'].replace(',', '')), reverse=True)
    return candidates[:5]

def run():
    now = datetime.now().strftime("%H:%M")
    stocks = get_closing_candidates()
    
    if not stocks:
        return

    msg = f"🎯 *[{now}] 종가매매/스윙 후보군*\n"
    msg += "_거래량 상위 +7~20% 상승 종목_\n\n"
    
    for i, s in enumerate(stocks):
        msg += f"{i+1}. *{s['name']}*\n"
        msg += f"💰 현재가: {s['price']}원 (+{s['change']}%)\n"
        msg += f"📊 거래량: {s['volume']}\n\n"
        
    msg += "💡 *매수 전략*: 3:20분까지 힘이 유지되는지 확인 후 분할 매수"
    send(msg)
