import requests
import json

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