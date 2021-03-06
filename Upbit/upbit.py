import requests
import json
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# get exchanges krw
# https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD,FRX.KRWJPY,FRX.KRWCNY,FRX.KRWEUR
def get_usd_krw():
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange =requests.get(url, headers=headers).json()
    return exchange[0]['cashBuyingPrice']
#     return exchange[0]['basePrice']

# https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-BTC
def get_last_price(coin_name):
    url = 'https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-{coin_name}'.format(coin_name=coin_name)
    tickValue =  requests.get(url, headers=headers).json()
    return tickValue[0]['tradePrice']


# price name openingPrice, highPrice, lowPrice, tradePrice, candleDateTimeKst
def get_price(term, interval, coin_name, count, price_name='tradePrice'):
    url = "https://crix-api.upbit.com/v1/crix/candles/{term}/{interval}?code=CRIX.UPBIT.KRW-{coin_name}&count={count}".format( term = term, interval = interval, coin_name = coin_name, count = count)
    
    response =requests.get(url, headers=headers)
    try:
        price_data = response.json()
    except  json.decoder.JSONDecodeError:
        print("Decode Error : ", coin_name)
        response.encoding = None
        price_data = response.json()
        
    price_list = []
    for item in price_data:
        code = item['code']
        code2 = code.replace("CRIX.UPBIT.KRW-", "")
        price = item[price_name]
        if 'KRW' in code:
            price_list.insert(0, price)
    
    return price_list

# make request url list
def make_url_list(interval, coin_name):
    num_req_count = 100
    #end_date = datetime.datetime(2017,10,1,0,0)
    end_date = datetime.datetime(2018,1,10,0,0)
    delta_time = datetime.timedelta(minutes=(num_req_count*int(interval)))
    cur_date = datetime.datetime.now() - datetime.timedelta(hours=9) # UTC
    
    min_str = cur_date.strftime("%M")
    del_min = int(min_str)%int(interval)
    
    cur_date = cur_date - datetime.timedelta(minutes=del_min)
    
    url_list = []   
    req_date = cur_date
    while end_date < req_date:
        req_str_date = req_date.strftime("%Y-%m-%dT%H:%M:00.000Z")
        url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{interval}?code=CRIX.UPBIT.KRW-{coin_name}&count={num_req_count}&to={req_str_date}'.format(interval=interval, coin_name=coin_name, num_req_count=num_req_count, req_str_date=req_str_date)
        url_list.append(url)
        req_date = req_date - delta_time
    return url_list

# return dict
def get_price_min(interval='60', coin_name='BTC'):
    url_list = make_url_list(interval, coin_name)
    open_price_list = [] # open price
    high_price_list = [] # high price
    low_price_list = [] # low price
    trade_price_list = [] # close price
    trade_volume_list = [] # Volume
    date_list = []
    for url in url_list:
        response = requests.get(url, headers=headers)
        price_data = response.json()
        
        for item in price_data:
            open_price_list.insert(0, item['openingPrice'])
            high_price_list.insert(0, item['highPrice'])
            low_price_list.insert(0, item['lowPrice'])
            trade_price_list.insert(0, item['tradePrice'])
            trade_volume_list.insert(0, item['candleAccTradeVolume'])
#             datetime.datetime.strptime(item['candleDateTimeKst'], '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
#             date_list.insert(0, item['candleDateTimeKst'])
            date_list.insert(0, datetime.datetime.strptime(item['candleDateTimeKst'], '%Y-%m-%dT%H:%M:%S+09:00').strftime("%Y-%m-%d %H:%M:%S"))

    return {'date': date_list, 'open': open_price_list, 'high':high_price_list, 'low':low_price_list, 'trade':trade_price_list, 'volume':trade_volume_list}
    
