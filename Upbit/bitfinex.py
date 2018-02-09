#_*_ coding:utf8 _*_
import requests
import json
import time
import datetime
import urllib.request
from bs4 import BeautifulSoup
import upbit

#https://api.bitfinex.com/v2/candles/trade::TimeFrame::Symbol/Section
# PATH PARAMS
#    TimeFrame(string) : '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M'
#    Symbol(string) : tBTCUSD
#    Section(string) : "last", "hist"
# QUERY PARAMS
#    limit(int32) : Number of candles requested
#    start(string) : Filter start (ms)
#    end(string) : Filter end (ms)
#    sort(int32) : if = 1 it sorts results returned with old > new
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def get_ticker(coin_name):
    url = "https://api.bitfinex.com/v2/ticker/{coin}".format(coin=coin_name)
    info = requests.get(url, headers=headers).json() # [BID ,BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW]
    # BID    float    Price of last highest bid
    # BID_SIZE    float    Size of the last highest bid
    # ASK    float    Price of last lowest ask
    # ASK_SIZE    float    Size of the last lowest ask
    # DAILY_CHANGE    float    Amount that the last price has changed since yesterday
    # DAILY_CHANGE_PERC    float    Amount that the price has changed expressed in percentage terms
    # LAST_PRICE    float    Price of the last trade
    # VOLUME    float    Daily volume
    # HIGH    float    Daily high
    # LOW    float    Daily low
    dict_info = {}
    keys = [ 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_PERC', 'LAST_PRICE', 'VOLUME', 'HIGH', 'LOW']
    idx = 0
    for key in keys:
        dict_info[key] = info[idx]
        idx = idx + 1
    return dict_info


time_19700101 = datetime.datetime(1970,1,1,0,0)
 
interval = '1m'
coin_name = 'tBTCUSD'
num_req_cout = 10
current_time = datetime.datetime.now()
start_date = datetime.datetime(2018,2,1,11,0) - datetime.timedelta(hours=9) # UTC
start_time_ms = int((start_date - time_19700101).total_seconds() * 1000)
 
def get_data(interval, count, coin_name, end_time_ms):
    url = ('https://api.bitfinex.com/v2/candles/trade:{TimeFrame}:{Symbol}/{Section}'
       .format(TimeFrame=interval, Symbol=coin_name, Section='hist'))
    query_param = {'limit': count, 'end': end_time_ms, 'sort': -1}
    
def get_candle(interval, count, coin_name, end_time_ms):
    url = ('https://api.bitfinex.com/v2/candles/trade:{TimeFrame}:{Symbol}/{Section}'
           .format(TimeFrame=interval, Symbol=coin_name, Section='hist'))
    query_param = {'limit': num_req_cout, 'end': start_time_ms, 'sort': -1}
    candles = requests.get(url, params = query_param, headers=headers).json()
 
url = ('https://api.bitfinex.com/v2/candles/trade:{TimeFrame}:{Symbol}/{Section}'
       .format(TimeFrame=interval, Symbol=coin_name, Section='hist'))
query_param = {'limit': num_req_cout, 'end': start_time_ms, 'sort': -1}
 
try:
    r = requests.get(url, params = query_param, headers=headers)
    data = r.json()
#     print(data)
except :
    print('fail')
 
last_date_ms = 0    
for item in data:
#     print(item[0])
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item[0]/1000)), 'Low : ', item[4])
    last_date_ms = item[0]
 
# last_date_ms = last_date_ms + (9*60*1000)
query_param = {'limit': num_req_cout, 'end': last_date_ms, 'sort': -1} 
 
print('End')
try:
    r = requests.get(url, params = query_param, headers=headers)
    data = r.json()
#     print(data)
except :
    print('fail')
 
last_date_ms = 0    
for item in data:
#     print(item[0])
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item[0]/1000)), 'Low : ', item[4])
    last_date_ms = item[0]
