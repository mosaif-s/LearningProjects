import requests
import datetime as dt
today = dt.date.today()
news_day = today - dt.timedelta(days=3)
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## Uses https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=ZZGKDYOR04TE051I'
r = requests.get(url)
data = r.json()
yesterdayDate=(list(data['Time Series (Daily)'].keys())[0])
DByesterdayDate=(list(data['Time Series (Daily)'].keys())[1])
yesterdayPrice=float(data['Time Series (Daily)'][yesterdayDate]['1. open'])
dayBeforeYesterdayPrice=float(data['Time Series (Daily)'][DByesterdayDate]['1. open'])
percentageChange=((yesterdayPrice-dayBeforeYesterdayPrice)/dayBeforeYesterdayPrice)*100

## Uses https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
API_key_news=""
url = ('https://newsapi.org/v2/everything?'
       'q=Tesla&'
       f'from={news_day}&'
       'sortBy=popularity&'
       f'apiKey={API_key_news}')

response = requests.get(url)
data=response.json()
top_3_articles = data['articles'][:3]
top_3 = [
    {
        'title': article['title'],
        'description': article['description'],
    }
    for article in top_3_articles
]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
for i in range(3):
    message=(f""
             f" {STOCK} : {percentageChange:.2f}%\n"
             f" Headline: {(top_3[i]['title'])}\n"
             f" Brief: {(top_3[i]['description'])} ")
    print(message)
# Message would be formatted like this if using a messaging API
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

