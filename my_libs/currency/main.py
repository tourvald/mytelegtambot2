import chat_analysis

if __name__ == '__main__':
    chat_analysis.start_export()
    raw_price_list = chat_analysis.analyze_main()
    dates_and_rates = chat_analysis.calculate_daily_average(raw_price_list)
    print(dates_and_rates)
    chat_analysis.update_currency_rates(dates_and_rates)
