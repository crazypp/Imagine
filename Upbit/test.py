import requests
import json
import upbit
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
def get_price_min(interval='60', coin_name='ADA', price_name='tradePrice'):
    url_list = upbit.make_url_list(interval, coin_name)
    data = {}
    price_list = []
    date_list = []
    for url in url_list:
        print(url)
        response = requests.get(url, headers=headers)
        price_data = response.json()

        for item in price_data:
            code = item['code']
            price = item[price_name]
            dateKst = item['candleDateTimeKst']
            if 'KRW' in code:
                price_list.insert(0, price)
                date_list.insert(0, dateKst)
     
    data = {'date': date_list, 'price': price_list}
#     idx = 0
#     for price in price_list:
#         print('i=', idx, 'Day=',date_list[idx], ' Price=', price_list[idx])
#         idx = idx + 1
    return data
        

data_dic = get_price_min()
list1 = data_dic['date']
list2 = data_dic['price']
print(list1.__len__())
# idx = 0
# for p in list1:
#     print(list1[idx],'  ',list2[idx])
#     idx = idx+1
