import datetime
from datetime import timezone, timedelta
import us_market
import surge_stock

def main():
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    # 시간을 따지지 않고 두 개 다 강제로 실행해보기
    print("테스트 모드: 모든 기능을 실행합니다.")
    us_market.run()
    surge_stock.run()

# 👇 파이썬에게 "이 파일이 열리면 main() 함수를 실행해!"라고 명령하는 핵심 코드입니다.
if __name__ == "__main__":
    main()
