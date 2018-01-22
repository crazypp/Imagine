import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fbprophet import Prophet

import upbit

btc_price = upbit.get_price(term='minutes', interval='60', coin_name='BTC', count='200', price_name='tradePrice')
xrp_price = upbit.get_price(term='minutes', interval='60', coin_name='XRP', count='200', price_name='tradePrice')


x = np.arange(0, 200, 1)
btc_1 = np.array(btc_price)
btc_price2 = btc_1/10000

plt.plot(x, xrp_price, 'r', lw=2, label='xrp')
plt.plot(x, btc_price2, 'b', lw=2, label='btc')
#plt.plot(x, y1, 'b', lw=2, label='btc')
#plt.plot(x, y2, 'y', lw=2, label='ada')
plt.grid()
plt.legend(loc='best')
plt.show()