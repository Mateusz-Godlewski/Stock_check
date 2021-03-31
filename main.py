import requests
import datetime

STOCK = input("Enter ticker: ").upper()
time_now = datetime.datetime.now()
date_yesterday = time_now.replace(day=time_now.day - 1)
date_before_yesterday = date_yesterday.replace(day=date_yesterday.day - 1)
proper_yesterday = str(date_yesterday.date())
proper_before_yesterday = str(date_before_yesterday.date())

# TODO 1 REPLACE ALPHA VANTAGE KEY
alpha_vantage_key = "ALPHA VANTAGE KEY GOES HERE"
alpha_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": alpha_vantage_key,
}
response_alpha = requests.get(url="https://www.alphavantage.co/query", params=alpha_params)
response_alpha.raise_for_status()

# TODO 2 REPLACE NEWSAPI KEY
news_key = "NEWSAPI KEY GOES HERE"
news_params = {
    "apiKey": news_key,
    "q": STOCK,
}
response_news = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
response_news.raise_for_status()

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
close_yesterday = float(response_alpha.json()["Time Series (Daily)"][proper_yesterday]["4. close"])
close_before_yesterday = float(response_alpha.json()["Time Series (Daily)"][proper_before_yesterday]["4. close"])
daily_change_percentage = round(close_yesterday / close_before_yesterday * 100 - 100, 2)

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if daily_change_percentage > 0:
    print(f"{STOCK} has risen {daily_change_percentage}%\n")
elif daily_change_percentage < 0:
    print(f"{STOCK} has fallen {daily_change_percentage}%\n")
else:
    print(f"{STOCK}'s daily change is {daily_change_percentage}%\n")
for i in range(3):
    print(f'{response_news.json()["articles"][i]["source"]["name"]}:')
    print(response_news.json()["articles"][i]["title"])
    try:
        print(response_news.json()["articles"][i]["description"].replace("Summary List Placement", ""))
    except AttributeError:
        print(f"\n\nI'm sorry but I could not find relevant news considering {STOCK}.\nThe above might not be of interest.")
    print()
