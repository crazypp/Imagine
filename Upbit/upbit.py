import requests
import json
import datetime

# price name openingPrice, highPrice, lowPrice, tradePrice, candleDateTimeKst
def get_price(term, interval, coin_name, count, price_name='tradePrice'):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
    start_time = datetime.datetime(2018,1,17,0,0)
    end_time = datetime.datetime.now()
    num_dates = end_time-start_time
    num_hours = (num_dates.days*24) + (num_dates.seconds//3600)
    num_req = num_hours//num_req_count
    num_req_remain = num_hours%num_req_count
    delta_hour = datetime.timedelta(hours=num_req_count)
    req_date = start_time
    url_list = []
    for i in range(0, num_req+1):
        req_str_date = req_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{interval}?code=CRIX.UPBIT.KRW-{coin_name}&count={num_req_count}&to={req_str_date}'.format(interval=interval, coin_name=coin_name, num_req_count=num_req_count, req_str_date=req_str_date)
        url_list.append(url)
        req_date = req_date + delta_hour
    return url_list

