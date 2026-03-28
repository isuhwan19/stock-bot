import datetime
# 👇 이 부분이 빠져서 에러가 났던 거예요! 추가했습니다.
from datetime import timezone, timedelta
import us_market
import surge_stock

def main():
    # 이제 timezone과 timedelta를 인식할 수 있습니다.
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    print(f"현재 한국 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 테스트를 위해 강제로 실행하도록 설정된 상태입니다.
    print("테스트 실행: surge_stock.run()을 호출합니다.")
    surge_stock.run()

if __name__ == "__main__":
    main()
