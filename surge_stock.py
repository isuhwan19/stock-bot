from telegram import send

def run():
    stocks = [
        {"name": "테스트종목", "change": 4.5},
    ]

    for stock in stocks:
        if stock["change"] > 3:
            send(f"🔥 급등 감지: {stock['name']} +{stock['change']}%")
