# LSTM(Long-Short Term Memory)

import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error
import upbit


# get coin data
ada_dict = upbit.get_price_min('60', 'ADA')
# 'date': date_list
# 'open': open price
# 'high': high price
# 'low': low price
# 'trade': end price
# 'volume': volume
date_list = ada_dict['date']
price_list = ada_dict['trade']

# convert nparray
price_array = np.array(price_list)
price_array.astype('float32')
#print(price_array)

# normalization
scaler = MinMaxScaler(feature_range=(0, 1))
nptf = scaler.fit_transform(price_array)

# split train, test
# train_size = int(len(nptf) * 0.9)
# test_size = len(nptf) - train_size
# train, test = nptf[0:train_size], nptf[train_size:len(nptf)]
# print(len(train), len(test))