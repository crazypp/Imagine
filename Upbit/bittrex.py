#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-ADA&tickInterval=thirtyMin
#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-ADA&tickInterval=hour
#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-ADA&tickInterval=fiveMin

#https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/5?code=CRIX.UPBIT.KRW-ADA&count=100&to=2018-01-28T12:45:00.000Z
import requests
import json
import datetime
import upbit

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_price_5min(coin_name):
    url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-{coin_name}&tickInterval=fiveMin'.format(coin_name=coin_name)
    
    response = requests.get(url, headers=headers)
    price_data = response.json()
    price_data = price_data['result']
    
    open_price_list = [] # open price
    high_price_list = [] # high price
    low_price_list = [] # low price
    trade_price_list = [] # close price
    trade_volume_list = [] # Volume
    date_list = []
    for item in price_data:
        open_price_list.append(item['O'])
        high_price_list.append(item['H'])
        low_price_list.append(item['L'])
        trade_price_list.append(item['C'])
        trade_volume_list.append(item['V'])
        date_list.append((datetime.datetime.strptime(item['T'], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")) # UTC to KST
    return {'date': date_list, 'open': open_price_list, 'high':high_price_list, 'low':low_price_list, 'trade':trade_price_list, 'volume':trade_volume_list}

interval='5'
coin_name = 'ADA'
urls = upbit.make_url_list(interval, coin_name)

open_price_list = [] # open price
high_price_list = [] # high price
low_price_list = [] # low price
trade_price_list = [] # close price
trade_volume_list = [] # Volume
date_list = []
for url in urls:
    delta_5min = datetime.timedelta(minutes=5)
    data_list = requests.get(url, headers=headers).json()
    prev_date = datetime.datetime.strptime(url, 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/5?code=CRIX.UPBIT.KRW-ADA&count=100&to=%Y-%m-%dT%H:%M:00.000Z')
    prev_date = prev_date + datetime.timedelta(hours=9) - delta_5min
    for data in data_list:
        date = datetime.datetime.strptime(data['candleDateTimeKst'], '%Y-%m-%dT%H:%M:%S+09:00') # kst time
        expected_date = prev_date - delta_5min
        if date != expected_date: # fix the data
            date_str = (expected_date + delta_5min).strftime("%Y-%m-%dT%H:%M:00.000Z")
            #https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/5?code=CRIX.UPBIT.KRW-ADA&count=100&to=2018-01-28T12:45:00.000Z
            url1 = ('https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{interval}?code=CRIX.UPBIT.KRW-{coin_name}&count=1&to={utc_date}'
                    .format(interval=interval, coin_name=coin_name, utc_date=date_str))
            data = requests.get(url1, headers=headers).json()
            data = data[0]

        open_price_list.insert(0, data['openingPrice'])
        high_price_list.insert(0, data['highPrice'])
        low_price_list.insert(0, data['lowPrice'])
        trade_price_list.insert(0, data['tradePrice'])
        trade_volume_list.insert(0, data['candleAccTradeVolume'])
        date_list.insert(0, datetime.datetime.strptime(data['candleDateTimeKst'], '%Y-%m-%dT%H:%M:%S+09:00').strftime("%Y-%m-%d %H:%M:%S"))
        prev_date = expected_date
        

#---------------------------------------------------------------------------------
# for i in range(95, 105, 1):
#     print('(%d) : Kst(%s) UTC(%s)'% (i, date_list[i]['candleDateTimeKst'], date_list[i]['candleDateTime']))

# upbit_ada_dict = upbit.get_price_min('5', 'ADA')
# bitrex_ada_dic = get_price_5min('ADA')
# 
# date_list1 = upbit_ada_dict['date']
# date_list2 = bitrex_ada_dic['date']
# date_list2 = date_list2[-len(date_list1):]
# 
# for i in range(len(date_list1)-1,0,-1):
#     if date_list1[i] != date_list2[i]:
#         print('%d is diff up[%s], bit[%s]'% (i, date_list1[i], date_list2[i]))
#         break
# print('upbit len=', len(date_list1))
# print('bitr len=', len(date_list2))
# print('upbit=', date_list1[-1])
# print('bitrex=' , date_list2[-1])
# print('upbit=', date_list1[-2])
# print('bitrex=' , date_list2[-2])
# 
# print('upbit=', date_list1[0])
# print('bitrex=' , date_list2[0])
# print('tt=', date_list2)