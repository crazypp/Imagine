import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fbprophet import Prophet

import upbit

# price name openingPrice, highPrice, lowPrice, tradePrice, candleDateTimeKst
#btc_price = upbit.get_price(term='minutes', interval='60', coin_name='BTC', count='200', price_name='tradePrice')
ada_price = upbit.get_price(term='minutes', interval='60', coin_name='ADA', count='200', price_name='tradePrice')
time_stamp = upbit.get_price(term='minutes', interval='60', coin_name='ADA', count='200', price_name='candleDateTimeKst')

#xrp_price = list(map(int, xrp_price))
#print(xrp_price)

#x = np.arange(0, 224, 1)
#x_date = pd.date_range('2018-01-14 17:00:00', periods=200, freq='h')
#print(x_date)
#btc_1 = np.array(btc_price)
#btc_price2 = btc_1/10000

#plt.plot(x, xrp_price, 'r', lw=2, label='xrp')
#plt.plot(x, btc_price2, 'b', lw=2, label='btc')
#plt.plot(x, y1, 'b', lw=2, label='btc')
#plt.plot(x, y2, 'y', lw=2, label='ada')
#plt.grid()
#plt.legend(loc='best')
#plt.show()

date = time_stamp[0][:10]
hour1 = int(time_stamp[0][11:13])
hour = str(hour1)+':00:00'
start_time = date +' '+hour
#df = pd.DataFrame({'ds':pd.date_range('2018-01-14 17:00:00', periods=200, freq='h'), 'y':xrp_price})
df = pd.DataFrame({'ds':pd.date_range(start_time, periods=200, freq='h'), 'y':ada_price})
#df = pd.DataFrame({'ds':time_stamp, 'y':xrp_price})
#df.reset_index(inplace=True)
#df.head()
#print(df)

#m = Prophet(yearly_seasonality=False, weekly_seasonality=False)
m = Prophet(yearly_seasonality=False, weekly_seasonality=True)
m.fit(df)

future_dates = m.make_future_dataframe(freq='h',periods=48)

forecast = m.predict(future_dates)
#m.plot(forecast)
#m.plot_components(forecast)
#print(forecast)
#plt.show()

#x = pd.date_range(start_time, periods=200, freq='h')
#x = x + future_dates
#print("x=", x)
#plt.plot(x, ada_price, 'r', lw=2, label='ADA')
#plt.grid()
#plt.legend(loc='best')
#plt.show()