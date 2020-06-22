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
from plotly import graph_objs as go
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs
from scipy.optimize import minimize
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from scipy.optimize import curve_fit
from IPython.display import clear_output

def moving_average(series, n):
      return np.average(series[-n:])


def weighted_average(series, weights):
    result = 0.0
    weights.reverse()
    for n in range(len(weights)):
        result += series[-n - 1] * weights[n]
    return result


def exponential_smoothing(series, alpha):
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result


def double_exponential_smoothing(series, alpha, beta):
    result = [series[0]]
    for n in range(1, len(series) + 1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series):  # прогнозируем
            value = result[-1]
        else:
            value = series[n]
        last_level, level = level, alpha * value + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        result.append(level + trend)
    return result


def plotly_df(df, title=''):
    data = []

    for column in df.columns:
        trace = go.Scatter(
            x=df.index,
            y=df[column],
            mode='lines',
            name=column
        )
        data.append(trace)

    layout = dict(title=title)
    fig = dict(data=data, layout=layout)
    iplot(fig, show_link=False)
    plt.show()


def TimeSeries(): #случай для Алабамы
    plot_data = pd.read_excel('Data.xlsx', usecols=['Date', 'Province/State', 'positive'], index_col=[0], parse_date=[0], nrows = 125)
    plot_data.drop(['Province/State'], axis=1, inplace=True)
    plot_data = plot_data.loc[~plot_data['positive'].isin([0])]
    plot_array = plot_data['positive'].tolist()

    #результат скользящей средней с учетом 5 дней
    print(moving_average(plot_data.positive, 5), ' -moving average')

    #результат взвешенной средней с различными весами для 5 дней
    print(weighted_average(plot_array, [0.75, 0.1, 0.7, 0.05, 0.03]), ' -weighted_average')

def Smoothing():    #модель Хольта Винтерса c графическим отображением
    plot_data = pd.read_excel('Data.xlsx', usecols=['Date', 'Province/State', 'positive'], index_col=[0],
                              parse_date=[0], nrows=125)
    plot_data.drop(['Province/State'], axis=1, inplace=True)
    plot_data = plot_data.loc[~plot_data['positive'].isin([0])]
    plot_array = plot_data['positive'].tolist()
    with plt.style.context('seaborn-white'):
        plt.figure(figsize=(20, 8))
        for alpha in [0.3, 0.05]:
            plt.plot(exponential_smoothing(plot_array, alpha), label="Alpha {}".format(alpha))
            print(exponential_smoothing(plot_array, alpha))
        plt.plot(plot_array, "c", label="Actual")
        plt.legend(loc="best")
        plt.axis('tight')
        plt.title("Exponential Smoothing")
        plt.grid(True)
        plt.show()

def DoubleSmoothing():
    #двойное экспоненциальное сглаживание

    plot_data = pd.read_excel('Data.xlsx', usecols=['Date', 'Province/State', 'positive'], index_col=[0],
                              parse_date=[0], nrows=125)
    plot_data.drop(['Province/State'], axis=1, inplace=True)
    plot_data = plot_data.loc[~plot_data['positive'].isin([0])]
    plot_array = plot_data['positive'].tolist()

    with plt.style.context('seaborn-white'):
        plt.figure(figsize=(20, 8))
        for alpha in [0.9, 0.02]:
            for beta in [0.9, 0.02]:
                plt.plot(double_exponential_smoothing(plot_array, alpha, beta),
                         label="Alpha {}, beta {}".format(alpha, beta))
                print((double_exponential_smoothing(plot_array, alpha, beta)))

        plt.plot(plot_array, label="Actual")
        plt.legend(loc="best")
        plt.axis('tight')
        plt.title("Double Exponential Smoothing")
        plt.grid(True)
        plt.show()

def file_read(name):
    plot_data = pd.read_excel(name, usecols=['Date', 'Province/State', 'positive'])
    return plot_data

def States(dataf):
    state_list = dataf.iloc[:, 1].astype(str)
    state_list = state_list.drop_duplicates(keep='first')
    state_list = state_list.tolist()
    return  state_list

def exp(x,a,b):
    return b+np.exp(a*x)

def mape_vectorized_v2(a, b):
    mask = a != 0
    return (np.fabs(a - b)/a)[mask].mean()

def sigmoid(x, A, M, P):
    return A / (1 + M*np.exp(-P*x))

def ExpModel(plot_data, state_list):
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    t = 0
    for i in range(40):
        plot1 = plot_data.loc[plot_data['Province/State'] == state_list[i]]
        plot1.drop(['Province/State'], axis=1, inplace=True)
        plot1 = plot1.loc[~plot1['positive'].isin([0])]
        rand_no = np.random.randint(6)
        p_par, p_cov = curve_fit(exp, range(len(plot1.positive)), plot1.positive, p0=[1, 2], maxfev=1000)
        Y_fit = exp(range(len(plot1.positive) + 10), p_par[0], p_par[1])
        fig = plt.figure(figsize=(18, 6))
        plt.plot(range(len(plot1.positive)), plot1.positive, '-o', color=color_list[rand_no])
        plt.plot(range(len(plot1.positive) + 10), Y_fit, '-o', color=color_list[rand_no + 1])
        plt.title('Covid-19 Plot for ' + state_list[i])
        plt.legend(['Actuals', 'Prediction of cases'])
        plt.show()
        #time.sleep(4)
        plt.clf()
        clear_output(wait=True)
        #print(Y_fit)


def SigmoidModel(plot_data, state_list):
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    t = 0
    Prediction = pd.DataFrame({'Alabama':[0,0,0,0,0,0,0,0,0,0]})

    for i in range(45):
        plot1 = plot_data.loc[plot_data['Province/State'] == state_list[i]]
        plot1.drop(['Province/State'], axis=1, inplace=True)
        plot1 = plot1.loc[~plot1['positive'].isin([0])]
        rand_no = np.random.randint(6)

        p_par, p_cov = curve_fit(sigmoid, range(len(plot1.positive)), plot1.positive, p0=[1, 2, 3], maxfev=1000)
        Y_fit = sigmoid(range(len(plot1.positive) + 10), p_par[0], p_par[1], p_par[2])

        fig = plt.figure(figsize=(18, 6))
        #plt.plot(range(len(plot1.positive)), plot1.positive, '-o', color=color_list[rand_no])
        #plt.plot(range(len(plot1.positive) + 10), Y_fit, '-o', color=color_list[rand_no + 1])
        #plt.title('Covid-19 Plot for ' + state_list[i])
        #plt.legend(['Actuals', 'curve_fit'])
        #plt.show()
        Prediction[state_list[i]] = Y_fit[-10:]
        #print(len(Y_fit[-10:]))
        #t = t + mape_vectorized_v2(plot1.positive, Y_fit[:len(plot1.positive)])
        #time.sleep(2)
        #plt.clf()
        #clear_output(wait=True)
    return Prediction

def Scikit():
    data = pd.read_excel('Data.xlsx', nrows = 125)
    one_state = data #Alabama
    state_positive = one_state['positive'].tolist()
    state_death = one_state['deaths'].tolist()
    x = data.drop(['positive', 'Province/State'], axis=1)
    state_positive = np.array(state_positive).reshape(-1, 1)
    state_death = np.array(state_death).reshape(-1, 1)

    date = list(range(0, 125))
    x['Date'] = date
    x = np.array(x)


    days_in_future = 20
    future_forecast = np.array([i for i in range(125 + days_in_future)]).reshape(-1, 1)
    adjusted_dates = future_forecast[:-20]

    X_train_positive, X_test_positive, y_train_positive, y_test_positive = train_test_split(x, state_positive, test_size=0.25, shuffle=False)
    poly = PolynomialFeatures(degree=3)
    poly_X_train_positive = poly.fit_transform(X_train_positive)
    poly_X_test_positive = poly.fit_transform(X_test_positive)
    poly_future_forecast = poly.fit_transform(future_forecast)

    linear_model = LinearRegression(normalize=True, fit_intercept=False)
    linear_model.fit(poly_X_train_positive, y_train_positive)
    test_linear_pred = linear_model.predict(poly_X_test_positive)
    print('MAE:', mean_absolute_error(test_linear_pred, y_test_positive))
    print('MSE:', mean_squared_error(test_linear_pred, y_test_positive))

def main():
    datasig = file_read('Data.xlsx')
    states = States(datasig)

    #DoubleSmoothing()
    #Smoothing()
    #TimeSeries()
    #SigmoidModel(datasig, states)
    #ExpModel(datasig, states)
    pred = SigmoidModel(datasig,states)
    pred.to_excel('Input.xlsx', startrow=0, index=False)
    #Scikit()

if __name__ == '__main__':
    main()
