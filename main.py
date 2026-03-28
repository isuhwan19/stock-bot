import datetime
from datetime import timezone, timedelta
import us_market
import surge_stock

def main():
    # 1. 한국 시간(KST) 세팅: UTC 시간보다 9시간 빠름
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    # Actions 로그에서 확인하기 좋게 현재 시간 출력
    print(f"현재 한국 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"현재 시간(시): {now.hour}")

    # 👉 아침 (미국 증시 리포트)
    if now.hour == 8:
        print("미국 증시 리포트를 실행합니다.")
        us_market.run()  # ⚠️ 주의: us_market.py 안의 함수 이름이 run()이어야 합니다!

    # 👉 장중 (급등주 감지)
    elif 9 <= now.hour <= 15:
        print("급등주 감지를 실행합니다.")
        surge_stock.run()
        
    else:
        print("지금은 알림을 보낼 시간이 아닙니다.")

if __name__ == "__main__":
    main()
