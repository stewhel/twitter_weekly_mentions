import requests
import os
import json
import pandas as pd
import yagmail
import datetime as dt
import time
from premailer import transform

global df

bearer_token = "AAAAAAAAAAAAAAAAAAAAAI%2FbdAEAAAAA94HllKR3SGGEXTiEIt8ReB7UZrs%3DX7E9ywlNDHnZhGcBp16zQmBbrDJ3uFMplifbokkJUvFhAdsC9e"
search_url = "https://api.twitter.com/2/tweets/counts/recent"

terms = ['NVDA', 'AMD', 'Semiconductor', 'Intel', 'Chips', 'Gaming']

dict2 = {}
list2 = []
df = pd.DataFrame(columns= terms)

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main(x):
    global data
    global df
    json_response = connect_to_endpoint(search_url, {'query': x + ' -is:retweet lang:en', 'granularity': 'day'})    
    data = json.dumps(json_response, indent=6, sort_keys=True)
    data = json.loads(data)
    df2 = pd.DataFrame.from_dict(data['data'])
    df2 = df2.rename(columns={'tweet_count': x})
    if len(list2) == 0:
        df2 = df2[['start', x]]
        list2.append(df2[['start', x]])
        
    else:
        df2 = df2[[x]]
        list2.append(df2[[x]])
    
for term in terms:
    main(term)
    
result_1 = pd.concat(list2, axis=1, ignore_index = False)
df = result_1

df = df.rename(columns={'start': 'Date'})
df['Date'] = df['Date'].str[0:-1]
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
df['Date'] = df['Date'].dt.strftime('%A, %b %d').astype(str)

s = df.style
s.set_properties(**{
    'font-size': '11pt',
    'font-family': 'Calibri'
})
s.set_properties(**{'text-align': 'center'})
s.set_properties(**{'width': '150px'})

html = transform(s.hide_index().render().replace("\n", ""))
rt = "\n" + "Scan Time: " + time.strftime("%A %b %d %H:%M:%S %p")

yag = yagmail.SMTP('stewhel9', 'Spaceforce5')
yag.send(to='stewhel9@gmail.com',
         subject='Weekly Twitter Mentions',
         contents= html + rt)
