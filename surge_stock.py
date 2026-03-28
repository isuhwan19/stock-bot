def run():
    now = datetime.now().strftime("%H:%M")
    stocks = get_closing_candidates()
    
    # 💡 테스트를 위해 데이터가 없어도 가짜 데이터를 넣어서 보내보기
    if not stocks:
        print("주말이라 데이터가 없네요! 테스트 데이터를 생성합니다.")
        stocks = [
            {"name": "주말테스트A", "price": "10,000", "change": 15.5, "volume": "1,200,000"},
            {"name": "주말테스트B", "price": "5,500", "change": 8.2, "volume": "800,000"}
        ]

    msg = f"🎯 *[{now}] 종가매매/스윙 후보군*\n"
    # ... 이하 동일
