import datetime
from datetime import timezone, timedelta
import us_market
import surge_stock

def main():
    # 1. 한국 시간(KST) 설정
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    print(f"현재 한국 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 👉 [오전 8시] 미국 증시 마감 리포트 전송
    if now.hour == 8:
        print("오전 8시: 미국 증시 리포트를 실행합니다.")
        us_market.run()

    # 👉 [오후 3시(15시)] 종가매매 및 스윙 종목 분석
    # (GitHub Actions 지연을 고려해 15시부터 16시 사이면 실행되도록 넉넉하게 잡았습니다.)
    elif 15 <= now.hour <= 16:
        print("오후 3시: 종가매매 감지 시스템을 실행합니다.")
        surge_stock.run()
        
    else:
        print(f"현재 시간({now.hour}시)은 알림 예약 시간이 아닙니다. 다음 스케줄을 기다립니다.")

if __name__ == "__main__":
    main()
