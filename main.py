import datetime
import us_market
import surge_stock

def main():
    now = datetime.datetime.now()

    # 👉 아침 (미국 증시 리포트)
    if now.hour == 8:
        us_market.run()

    # 👉 장중 (급등주 감지)
    elif 9 <= now.hour <= 15:
        surge_stock.run()

if __name__ == "__main__":
    main()
