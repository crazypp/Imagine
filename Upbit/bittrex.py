#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-ADA&tickInterval=thirtyMin
#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-ADA&tickInterval=hour
#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=USDT-ADA&tickInterval=fiveMin
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

urls = upbit.make_url_list('5', 'ADA')
 
idx = 0
last_time2 = datetime.datetime.now()
for url in urls:
    print('(%d) url=%s'%(idx, url))
    data = requests.get(url, headers=headers).json()
    print('len(%d) first=[%s], last=[%s]'% (len(data), data[0]['candleDateTimeKst'], data[-1]['candleDateTimeKst']))
    first_time = datetime.datetime.strptime(data[0]['candleDateTimeKst'], '%Y-%m-%dT%H:%M:%S+09:00')
    last_time = datetime.datetime.strptime(data[-1]['candleDateTimeKst'], '%Y-%m-%dT%H:%M:%S+09:00')
    if first_time != last_time2:
        print('%d th not same'% idx)
     
    last_time2 = last_time - datetime.timedelta(minutes=5)
 
    idx = idx + 1


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