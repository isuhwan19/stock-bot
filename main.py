import datetime
from datetime import timezone, timedelta
import us_market
import surge_stock

def main():
    # 1. 한국 시간(KST) 세팅 (UTC+9)
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    print(f"현재 한국 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 👉 [오전 8시] 미국 증시 마감 리포트 & 국장 대응 전략
    if now.hour == 8:
        print("미국 증시 리포트를 전송합니다.")
        us_market.run()

    # 👉 [오후 3시(15시)] 종가매매 및 스윙 종목 후보군 추출
    elif now.hour == 15:
        print("종가매매 후보 종목을 분석합니다.")
        surge_stock.run()
        
    # 👉 [그 외 시간] 로그만 남기고 종료
    else:
        print(f"현재 시간 {now.hour}시는 알림 예약 시간이 아닙니다.")

if __name__ == "__main__":
    main()
