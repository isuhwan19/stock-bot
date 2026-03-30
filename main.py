import datetime
from datetime import timezone, timedelta
import time
import us_market
import surge_stock

def wait_until(target_hour, target_minute):
    """목표 시간까지 10초 단위로 체크하며 정밀하게 대기"""
    KST = timezone(timedelta(hours=9))
    while True:
        now = datetime.datetime.now(KST)
        # 목표 시간에 도달하면 반복 종료
        if now.hour == target_hour and now.minute >= target_minute:
            break
        # 아직 시간이 안 됐으면 10초간 대기
        time.sleep(10)

def main():
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    current_hour = now.hour
    
    print(f"현재 실행 시각: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. [오전 8:00] 미국 증시 마감 리포트 (국장 개장 전 준비)
    # 7시 45분~8시 15분 사이에 서버가 깨어났을 때 작동
    if (current_hour == 7 and now.minute >= 40) or (current_hour == 8 and now.minute <= 15):
        print("오전 8시 정각까지 대기 후 미국 증시 리포트를 전송합니다...")
        wait_until(8, 0)
        us_market.run()

    # 2. [오후 3:10] 종가매매 분석 리포트 (정밀 실행)
    # 2시 50분~3시 20분 사이에 서버가 깨어났을 때 작동
    elif (current_hour == 14 and now.minute >= 50) or (current_hour == 15 and now.minute <= 20):
        print("오후 3시 10분 정각까지 대기 후 종가매매 분석을 시작합니다...")
        wait_until(15, 10)
        surge_stock.run()
        
    else:
        print(f"현재 시간({current_hour}시 {now.minute}분)은 예약된 실행 시간 범위가 아닙니다.")

if __name__ == "__main__":
    main()
