def main():
    KST = timezone(timedelta(hours=9))
    now = datetime.datetime.now(KST)
    
    print(f"현재 한국 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 💡 시간 조건을 무시하고 무조건 실행하도록 수정
    print("테스트 실행: surge_stock.run()을 강제로 호출합니다.")
    surge_stock.run()

if __name__ == "__main__":
    main()
