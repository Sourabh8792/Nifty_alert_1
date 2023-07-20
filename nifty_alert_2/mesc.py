import requests
from bs4 import BeautifulSoup
import pandas as pd

Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'

#You need to copy paste condition in below mentioned Condition variable
Condition = "( {33492} ( latest close < latest sma ( latest close , 20 ) ) ) "
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
print(data)

import pushbullet

# Set up Pushbullet configurations
api_key = "o.QjGRQWtZeY19TVnVPHM6iZ4ki6GBdOoc"
pb = pushbullet.Pushbullet(api_key)


if not data.empty:
    if 'MARUTI' in data['nsecode'].values:
        # Nifty is below 90-day moving average, send a push notification
        title = "Nifty Alert"
        message = "Nifty has closed below the 90-day moving average."
        if pb.push_note(title, message):
            print("Push notification sent successfully!")
        else:
            print("Push notification not sent!")
    else:
        print("Nifty is not present in the output")
else:
    print("The dataframe is empty")



