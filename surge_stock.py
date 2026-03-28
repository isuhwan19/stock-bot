import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone, timedelta

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def format_investor(val_str):
    """수급 데이터를 보기 좋게 [매수/매도]로 바꿔주는 함수"""
    try:
        val = int(val_str.replace(',', ''))
        if val > 0:
            return f"🔴 매수 (+{val_str}주)"
        elif val < 0:
            return f"🔵 매도 ({val_str}주)"
        else:
            return "보합 (0주)"
    except:
        return val_str

def get_investor_data(code):
    """해당 종목의 오늘(최근 거래일) 외국인/기관 순매수 데이터를 가져옵니다."""
    try:
        url = f"https://finance.naver.com/item/frgn.naver?code={code}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 투자자별 매매동향 테이블
        table = soup.find('table', {'class': 'type2'})
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            # 날짜, 종가, 전일비, 등락률, 거래량, 기관, 외인... (총 9개 칼럼)
            if len(cols) >= 9:
                inst_buy = cols[5].get_text(strip=True) # 기관 순매매량
                fore_buy = cols[6].get_text(strip=True) # 외국인 순매매량
                
                return format_investor(inst_buy), format_investor(fore_buy)
        return "정보없음", "정보없음"
    except Exception as e:
        return "조회실패", "조회실패"

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
            # a 태그 안에서 종목 코드를 빼냅니다 (수급 조회를 위해)
            a_tag = cols[1].find('a')
            if not a_tag: continue
            code = a_tag['href'].split('code=')[1]
            
            name = a_tag.get_text(strip=True)
            current_price = cols[2].get_text(strip=True)
            change_pct = float(cols[4].get_text(strip=True).replace('%', '').strip())
            volume = int(cols[5].get_text(strip=True).replace(',', ''))
            
            # 🔥 [종가매매 필터링 조건] (7~20% 상승, 50만주 이상 거래)
            if 7.0 <= change_pct <= 20.0 and volume >= 500000:
                candidates.append({
                    "name": name,
                    "code": code,
                    "price": current_price,
                    "change": change_pct,
                    "volume": volume
                })
        except (ValueError, IndexError):
            continue
            
    # 거래량 순으로 정렬하여 상위 5개만 추출
    candidates = sorted(candidates, key=lambda x: x['volume'], reverse=True)[:5]
    
    # 추출된 5개 종목에 대해서만 수급(외국인/기관) 데이터를 조회해서 합칩니다.
    for c in candidates:
        inst, fore = get_investor_data(c['code'])
        c['inst_buy'] = inst
        c['fore_buy'] = fore
        c['volume'] = format(c['volume'], ',') # 다시 보기 좋게 콤마 추가
        
    return candidates

def run():
    # 1. 한국 시간 설정
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    now_time = now.strftime("%H:%M")
    
    # 2. 주말 필터링 (월=0, 화=1, 수=2, 목=3, 금=4, 토=5, 일=6)
    if now.weekday() >= 5:
        msg = f"🛌 *[{now_time}] 봇 알림*\n\n"
        msg += "오늘은 주말이라 주식 시장이 열리지 않습니다.\n"
        msg += "푹 쉬시고 다음 주에 좋은 종목으로 찾아오겠습니다! ☕️"
        send(msg)
        return

    # 3. 평일일 경우 실제 데이터 크롤링
    stocks = get_closing_candidates()
    
    if not stocks:
        send(f"⚠️ *[{now_time}] 종가매매 감지*\n조건에 맞는 종목이 없습니다.")
        return

    msg = f"🎯 *[{now_time}] 종가매매/스윙 후보군*\n"
    msg += "_거래량 상위 +7~20% (수급 포함)_\n\n"
    
    for i, s in enumerate(stocks):
        msg += f"{i+1}. *{s['name']}*\n"
        msg += f"💰 현재가: {s['price']}원 (+{s['change']}%)\n"
        msg += f"📊 거래량: {s['volume']}주\n"
        msg += f"🏢 기관: {s['inst_buy']}\n"
        msg += f"🗽 외인: {s['fore_buy']}\n\n"
        
    msg += "💡 *매수 팁*: 외인/기관 양매수(🔴) 종목 위주로 일봉 차트 확인 후 접근!"
    send(msg)
