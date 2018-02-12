#_*_ coding:utf8 _*_
import requests
import json
import time
import datetime
import matplotlib.pyplot as plt
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


# get last block numer
# https://api.fork.lol/poll/last?t=1518397644
def get_last_block_num():
    timestamp = datetime.datetime.now().timestamp() # UTC
    timestamp = int(timestamp)
    url = "https://api.fork.lol/poll/last?t={timestamp}".format(timestamp = timestamp)
    print("Request Last Block Num. url=", url)
    last_blocks = requests.get(url, headers=headers).json() # last block number for BTC, BCH
    print("last block : ", last_blocks)
    return last_blocks
    
def get_info():
    # https://api.fork.lol/b508772-517029.fake.csv
    blocksNo = get_last_block_num()
    url = "https://api.fork.lol/b{BTCNO}-{BCHNO}.fake.csv".format(BTCNO=blocksNo['BTC'], BCHNO=blocksNo['BCH'])
    info = requests.get(url, headers=headers).json()
    print("Complete Dari info")
    return info

def get_candle(interval, count, coin_name, timestamp):
    url = ('https://api.bitfinex.com/v2/candles/trade:{TimeFrame}:{Symbol}/{Section}'
           .format(TimeFrame=interval, Symbol=coin_name, Section='hist'))
    query_param = {'limit': count, 'end': timestamp*1000, 'sort': -1}
    candles = requests.get(url, params = query_param, headers=headers).json()
    # candle data order : MTS, OPEN, CLOSE, HIGH, LOW, VOLUME
#     print(candles)
    return candles
    
# ca = get_candle('1m', 1, 'tBTCUSD', 1515834128)
# print(ca)
    
# LastBtcBlockNo = get_last_block_num('BTC')
# print(LastBtcBlockNo)

dari_info = get_info()
BtcDariHist = dari_info['BTC']['history']['all']
print(BtcDariHist)
 
# extract to List
timestamp = []
height=[]
blocks=[]
avg_diff=[]
rate=[]
reward_avg=[]
dari=[]
txs=[]
cdd=[]
ClosePrice=[]
for item in BtcDariHist:
    timestamp.insert(0, item['timestamp'])
    height.insert(0, item['height'])
    blocks.insert(0, item['blocks'])
    avg_diff.insert(0, item['avg_diff'])
    rate.insert(0, item['rate'])
    reward_avg.insert(0, item['reward_avg'])
    dari.insert(0, item['dari'])
    txs.insert(0, item['txs'])
    cdd.insert(0, item['cdd'])
    # get bitfinex price data
    candle = get_candle('1m', 1, 'tBTCUSD', item['timestamp'])
    ClosePrice = candle[0][2]
    

     
# change timestamp to date string
Dates = []
for item in timestamp:
    Dates.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item)))
 
# make DataFrame
dataFR = {'height':height, 'blocks':blocks, 'avg_diff':avg_diff, 'rate':rate, 'reward_avg':reward_avg, 'dari':dari, 'txs':txs, 'cdd':cdd, 'ClosePrice':ClosePrice}
    

plt.plot(Dates, dataFR['rate'])
plt.show()









