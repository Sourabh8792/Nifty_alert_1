import requests
from bs4 import BeautifulSoup
import pandas as pd
import pushbullet

Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'

# You need to copy paste condition in below mentioned Condition variable
Condition = "( {cash} ( ( {cash} ( ( {cash} ( ( ( ( latest max ( 220 , latest close ) - latest close ) * 100 ) / latest max ( 220 , latest close ) ) > 20 ) ) or ( {cash} ( latest close <= latest sma ( latest close , 33 ) * 0.99 ) ) ) ) ) ) "

def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)
        df = pd.DataFrame()
        for item in r.json()['data']:
            df = pd.concat([df, pd.DataFrame([item])], ignore_index=True)
    return df


data = GetDataFromChartink(Condition)
print(len(data.index))
print(data)

# Set up Pushbullet configurations
api_key = "o.QjGRQWtZeY19TVnVPHM6iZ4ki6GBdOoc"
pb = pushbullet.Pushbullet(api_key)

if not data.empty:
        # Nifty is below 180-day moving average, send a push notification
        title = "Sell Alert"
        message = "You have to rebalance the portfolio this week."
        pb.push_note(title, message)
        print("Push notification sent successfully!")
else:
    print("The dataframe is empty")
