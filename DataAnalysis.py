import numpy as np
import pandas as pd
import seaborn as sns
import xlrd
import os
from IPython.display import clear_output
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')


class DataAnalysis:
    df = ''

    def __init__(self, MainTable):
        self.MainTableName = MainTable
        self.read_data(self.MainTableName)

    def read_data(self, name):
        self.df = pd.read_excel(name)

    def visualisationPositive(self):
        color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        plot_data = pd.read_excel('Data.xlsx', usecols=['Date','Province/State', 'positive'])
        state_list = plot_data.iloc[:, 1].astype(str)
        state_list = state_list.drop_duplicates(keep='first')
        for i in range(len(state_list)):
            plot1 = plot_data.loc[plot_data['Province/State'] == state_list[i]]
            plot1.drop(['Province/State'], axis=1, inplace=True)
            plot1 = plot1.loc[~plot1['positive'].isin([0])]
            fig = plt.figure(figsize=(18, 6))
            plt.plot(range(len(plot1.positive)), plot1.positive, '-o', color=color_list[np.random.randint(7)])
            plt.title('Covid-19 Plot for ' + state_list[i])
            plt.show()
            plt.clf()
            clear_output(wait=True)

    def visualisationDeaths(self):
        color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        plot_data = pd.read_excel('Data.xlsx', usecols=['Date','Province/State', 'deaths'])
        state_list = plot_data.iloc[:, 1].astype(str)
        state_list = state_list.drop_duplicates(keep='first')
        for i in range(len(state_list)):
            plot1 = plot_data.loc[plot_data['Province/State'] == state_list[i]]
            plot1.drop(['Province/State'], axis=1, inplace=True)
            plot1 = plot1.loc[~plot1['deaths'].isin([0])]
            fig = plt.figure(figsize=(18, 6))
            plt.plot(range(len(plot1.deaths)), plot1.deaths, '-o', color=color_list[np.random.randint(7)])
            plt.title('Covid-19 Deaths for ' + state_list[i])
            plt.show()
            plt.clf()
            clear_output(wait=True)

    def mostCases(self):
        top = self.df[self.df['Date'] == self.df['Date'].max()]
        top.rename(columns={'Province/State': 'state'}, inplace=True)
        actives = top.groupby(by = 'state')['positive'].sum().sort_values(ascending=False).head(20).reset_index()
        #print(actives)
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel('Total cases', fontsize=30)
        plt.ylabel('State', fontsize=30)
        plt.title('Top 20 states having most active cases', fontsize=30)
        ax = sns.barplot(x=actives.positive, y=actives.state)
        for i, (value, name) in enumerate(zip(actives.positive, actives.state)):
            ax.text(value, i - 0.5, f'{value:.0f}', size=10, ha='left', va='center')
        print(ax.set(xlabel='Total cases', ylabel='State'))
        plt.show()

    def CompareCases(self):
        state_list = self.df.iloc[:, 2].astype(str)
        state_list = state_list.drop_duplicates(keep='first')
        state_list = state_list.tolist()
        states_positive = pd.DataFrame()
        for i in range(50):
            pred = self.df.loc[self.df['Province/State'] == state_list[i]]
            positive = pred['positive'].tolist()
            states_positive[state_list[i]] = positive

        for i in range(1, 5):
          plt.figure(figsize=(20, 6))
          for j in states_positive.columns[(i - 1) * 5:i * 5]:
            data = states_positive[[j]]
            data = data[data[j] > 0].reset_index(drop=True)
            data = data.rolling(2).mean().fillna(0)
            plt.plot([str(i) for i in data[j].index], data[j], marker='*', label=j)

        plt.title("STATE LEVEL CONFIRMED CASES GROWTH CURVE")
        plt.legend()
        plt.xlabel('Day')
        plt.ylabel('Confirmed Cases')
        plt.show()

        mse_list = []
        best_pair = {}

        for i in states_positive.columns:
            selected = []
            data = states_positive[[i]]
            data = states_positive[data[i] > 0].reset_index(drop=True)  # начинаем индекс, где нет нуля
            data_list1 = data.iloc[:, 0].values  # удаляем нулевые значения
            for j in states_positive.columns:
                if j != i:
                    data1 = states_positive[[j]]  # берем другой штат
                    data1 = data1[data1[j] > 0].reset_index(drop=True)  # начинаем индекс, где нет нуля
                    data_list2 = data1.iloc[:, 0].values  # удаляем нулевые значения
                    if len(data_list1) < len(data_list2):
                        corr = np.corrcoef(data_list1, data_list2[:len(data_list1)])[0, 1]
                        # print(corr, '-corr')
                        mse = (np.square(data_list1 - data_list2[:len(data_list1)])).mean()
                        # print(mse, '-mse')
                        mse_list.append(mse)
                        if ((mse < 150000) & (corr > .7)):
                            if len(data1[j]) > len(data[i] + 7):
                                plt.figure(figsize=(21, 6))
                                plt.plot([str(i) for i in data[i].index], data[i], marker='*', label=i)
                                plt.plot([str(i) for i in data1[j].index], data1[j], marker='*', label=j)
                                plt.title("Corrleation {},MSE {}".format(round(corr * 100, 2), mse))
                                plt.legend()
                                plt.xlabel('Day')
                                plt.ylabel('Confirmed Cases')
                                plt.show()
                                selected.append(data_list2[:len(data_list1) + 7])
            if len(selected) > 0:
                best_pair[i] = selected

    def Diagrams(self):
        #Средний возраст
        top = self.df[self.df['Date'] == self.df['Date'].max()]
        top.rename(columns={'Province/State': 'state'}, inplace=True)
        actives = top.groupby(by = 'state')['med_age'].sum().sort_values(ascending=False).head(20).reset_index()
        #print(actives)
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel('Media age', fontsize=30)
        plt.ylabel('State', fontsize=30)
        plt.title('Top 20 ', fontsize=30)
        ax = sns.barplot(x=actives.med_age, y=actives.state)
        for i, (value, name) in enumerate(zip(actives.med_age, actives.state)):
            ax.text(value, i - 0.5, f'{value:.0f}', size=10, ha='left', va='center')
        print(ax.set(xlabel='Median Age', ylabel='State'))
        plt.show()
        plt.clf()

        #страховка
        top = self.df[self.df['Date'] == self.df['Date'].max()]
        top.rename(columns={'Province/State': 'state'}, inplace=True)
        actives = top.groupby(by = 'state')['insurance'].sum().sort_values(ascending=False).head(20).reset_index()
        #print(actives)
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlabel('Insurance', fontsize=30)
        plt.ylabel('State', fontsize=30)
        plt.title('Top 20 ', fontsize=30)
        ax = sns.barplot(x=actives.insurance, y=actives.state)
        for i, (value, name) in enumerate(zip(actives.insurance, actives.state)):
            ax.text(value, i - 0.5, f'{value:.0f}', size=10, ha='left', va='center')
        print(ax.set(xlabel='Insurance', ylabel='State'))
        plt.show()
        plt.clf()

t = DataAnalysis('Data.xlsx')
#t.visualisationPositive()
#t.visualisationDeaths()
#t.mostCases()
#t.CompareCases()
#t.Diagrams()