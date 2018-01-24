import requests
import json
import upbit
import datetime

ada_dict = upbit.get_price_min('10', 'ADA')
date_list = ada_dict['date']
print('date size=',date_list.__len__())

for date in date_list:
    print(date)
