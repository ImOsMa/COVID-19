import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import math
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
import datetime
import operator
from collections import OrderedDict

df = pd.read_excel('Main.xlsx')
date = df['Date'].tolist()
date = list(OrderedDict.fromkeys(date))
days_since_1_22 = np.array([i for i in range(len(date))]).reshape(-1, 1)
pd.get_dummies(df['state'])

alabama = df[5875:5875+len(date)]
alabama_positive = alabama['positive'].tolist()
alabama_death = alabama['deaths'].tolist()
alabama_recovered = alabama['recovered'].tolist()
alabama_active = alabama['active'].tolist()

alabama_positive = np.array(alabama_positive).reshape(-1, 1)
alabama_death = np.array(alabama_death).reshape(-1, 1)
alabama_recovered = np.array(alabama_death).reshape(-1, 1)

days_in_future = 20
future_forecast = np.array([i for i in range(len(date)+days_in_future)]).reshape(-1,1)
adjusted_dates = future_forecast[:-20]

start = '2020-01-22'
start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
future_forecast_dates = []
for i in range(len(future_forecast)):
    future_forecast_dates.append((start_date + datetime.timedelta(days = i)).strftime('%Y-%m-%d'))
X_train_positive, X_test_positive, y_train_positive, y_test_positive = train_test_split(days_since_1_22, alabama_positive, test_size=0.25, shuffle = False)

#transform our data for polynomial regression
poly = PolynomialFeatures(degree=3)
poly_X_train_positive = poly.fit_transform(X_train_positive)
poly_X_test_positive = poly.fit_transform(X_test_positive)
poly_future_forecast = poly.fit_transform(future_forecast)

#polynomial regression
linear_model = LinearRegression(normalize=True, fit_intercept=False)
linear_model.fit(poly_X_train_positive, y_train_positive)
test_linear_pred = linear_model.predict(poly_X_test_positive)
linear_pred = linear_model.predict(poly_future_forecast)
print('MAE:', mean_absolute_error(test_linear_pred, y_test_positive))
print('MSE:', mean_squared_error(test_linear_pred, y_test_positive))