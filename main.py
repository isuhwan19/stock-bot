import datetime
from datetime import timezone, timedelta
import us_market
import surge_stock

def main():
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    print(f"현재 한국 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 👉 [오전 8시] 미국 증시 리포트
    if now.hour == 8:
        print("미국 증시 리포트를 실행합니다.")
        us_market.run()

    # 👉 [오후 3시(15시)] 종가매매 후보군 알림
    elif now.hour == 15:
        print("종가매매 감지를 실행합니다.")
        surge_stock.run()
        
    else:
        print(f"현재 시간({now.hour}시)은 알림 예약 시간이 아닙니다.")

if __name__ == "__main__":
    main()
