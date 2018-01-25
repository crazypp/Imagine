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
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import upbit

# The function takes two arguments: 
# the dataset, which is a NumPy array that we want to convert into a dataset, 
# and the look_back, which is the number of previous time steps to use as input variables to predict the next time period — in this case defaulted to 1.
#
# This default will create a dataset 
# where X is the number of passengers at a given time (t) and 
# Y is the number of passengers at the next time (t + 1).
look_back = 1
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


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
data_set = np.array(price_list)
data_set = data_set.reshape(price_list.__len__(), 1)
data_set.astype('float32')
# print(data_set)

# normalization
# LSTMs are sensitive to the scale of the input data, specifically 
# when the sigmoid (default) or tanh activation functions are used. 
# It can be a good practice to rescale the data to the range of 0-to-1, 
# also called normalizing. We can easily normalize the dataset using the MinMaxScaler preprocessing class from the scikit-learn library.
scaler = MinMaxScaler(feature_range=(0, 1))
nptf = scaler.fit_transform(data_set)

 
# split train, test
# With time series data, the sequence of values is important. 
# A simple method that we can use is to split the ordered dataset into train and test datasets. 
# The code below calculates the index of the split point and separates the data into the training datasets 
# with 80% of the observations that we can use to train our model, leaving the remaining 33% for testing the model.
train_size = int(len(nptf) * 0.8)
test_size = len(nptf) - train_size
train, test = nptf[0:train_size, :], nptf[train_size:len(nptf), :]
print('train len=%d, test len=%d'%(len(train), len(test)))
   
# create dataset for learning
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
   
#reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
   
# simple lstm network learning
# The network has a visible layer with 1 input, 
# a hidden layer with 4 LSTM blocks or neurons, 
# and an output layer that makes a single value prediction. 
# The default sigmoid activation function is used for the LSTM blocks. 
# The network is trained for 100 epochs and a batch size of 1 is used.
model = Sequential()
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=1500, batch_size=1, verbose=2)
   
# make prediction
# Note that we invert the predictions before calculating error scores 
# to ensure that performance is reported in the same units as the original data (thousands of passengers per month).
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
  
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
  
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
#testScore = math.sqrt(mean_squared_error(testY, testPredict))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % testScore)
  
# shift train predictions for plotting
# Because of how the dataset was prepared, 
# we must shift the predictions so that they align on the x-axis with the original dataset. 
# Once prepared, the data is plotted, showing the original dataset in blue, 
# the predictions for the training dataset in green, 
# and the predictions on the unseen test dataset in red.
trainPredictPlot = np.empty_like(nptf)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
# shift test predictions for plotting
testPredictPlot = np.empty_like(nptf)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(nptf)-1, :] = testPredict
 
print('nptf len=', len(nptf))
print('list len=', date_list.__len__())

lastX = nptf[-1]
for i in range(1, 48, 1):
    lastX = np.reshape(lastX, (1, 1, 1))
    lastY = model.predict(lastX)
    lastX = lastY # for re-predict
    lastY = scaler.inverse_transform(lastY)
    print('Predict the Close value of final time(%s)+%dh: %d' % (date_list[-1], i, lastY) )
# # predict last value (or tomorrow?)
# lastX = nptf[-1]
# lastX = np.reshape(lastX, (1, 1, 1))
# lastY = model.predict(lastX)
# lastX = lastY # for re-predict
# lastY = scaler.inverse_transform(lastY)
# print('Predict the Close value of final time(%s)+1h: %d' % (date_list[-1],lastY) )
# lastX = np.reshape(lastX, (1, 1, 1))
# lastY = model.predict(lastX)
# lastX = lastY # for re-predict
# lastY = scaler.inverse_transform(lastY)
# print('Predict the Close value of final time(%s)+2h: %d' % (date_list[-1],lastY) )
# lastX = np.reshape(lastX, (1, 1, 1))
# lastY = model.predict(lastX)
# lastX = lastY # for re-predict
# lastY = scaler.inverse_transform(lastY)
# print('Predict the Close value of final time(%s)+3h: %d' % (date_list[-1],lastY) )
 
# plot baseline and predictions
# plt.plot(date_list, scaler.inverse_transform(nptf), label='Org')
# plt.plot(trainPredictPlot, label='Train')
# plt.plot(testPredictPlot, label='Test')
# plt.grid()
# plt.legend()
# plt.tight_layout()
# plt.show()
 

