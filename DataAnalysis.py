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
import datetime
import operator
from collections import OrderedDict
import xlrd

df = pd.read_excel('Main.xlsx')
lockdown = pd.read_csv('Lockdowns.csv')
#print(df)
lockdown = lockdown.drop(['Sources'], axis = 1)
lockdown = lockdown.drop(['Gatherings banned'], axis = 1)
#print(lockdown)
emergency = lockdown['State of emergency declared'].tolist()
for i in range(len(emergency)):
    emergency[i] = emergency[i].replace('March ', '2020-03-')
    emergency[i] = emergency[i].replace('January ', '2020-01-')
    emergency[i] = emergency[i].replace('February ', '2020-02-')
lockdown['State of emergency declared'] = emergency
stay_at_home = lockdown['Stay at home ordered'].tolist()
for i in range(len(stay_at_home)):
    stay_at_home[i] = stay_at_home[i].replace('March ', '2020-03-').replace('(advisory)', '').replace(' (partial advisory)', '').replace(' (declared unconstitutional on May 13)', '').replace('Regional', '2020-12-01')
    stay_at_home[i] = stay_at_home[i].replace('January ', '2020-01-').replace('(advisory)', '').replace(' (partial advisory)', '').replace(' (declared unconstitutional on May 13)', '').replace('Regional', '2020-12-01')
    stay_at_home[i] = stay_at_home[i].replace('April ', '2020-04-').replace('(advisory)', '').replace(' (partial advisory)', '').replace(' (declared unconstitutional on May 13)', '').replace('Regional', '2020-12-01')
    stay_at_home[i] = stay_at_home[i].replace('No', '2020-12-01')
lockdown['Stay at home ordered'] = stay_at_home
print(stay_at_home)
out = lockdown['Out-of-state travel restrictions'].tolist()
for i in range(len(out)):
    out[i] = out[i].replace('No', '0')
    out[i] = out[i].replace('Mandatory quarantine', '2')
    out[i] = out[i].replace('Travel suspended', '2')
    out[i] = out[i].replace('Limited quarantine', '1')
    out[i] = out[i].replace('Recommended quarantine', '1')
    out[i] = out[i].replace(' / Screened', '')
    out[i] = out[i].replace('Regional', '1')
    out[i] = out[i].replace('Screened', '1')
lockdown['Out-of-state travel restrictions'] = out

schools = lockdown['Schools'].tolist()
daycares = lockdown['Daycares'].tolist()
bars = lockdown['Bars & sit-down restaurants'].tolist()
retail = lockdown['Non-essential retail'].tolist()

for i in range(len(schools)):
    schools[i] = schools[i].replace('Yes', '1').replace(' (remainder of term)','').replace('No', '0').replace('Regional', '0.5').replace('Restricted', '0.5').replace(' (districts choice)', '')
    daycares[i] = daycares[i].replace('Yes', '1').replace(' (remainder of term)', '').replace('No', '0').replace('Regional', '0.5').replace('Restricted', '0.5').replace(' (districts choice)', '')
    bars[i] = bars[i].replace('Yes', '1').replace(' (remainder of term)', '').replace('No', '0').replace('Regional', '0.5').replace('Restricted', '0.5').replace(' (districts choice)', '')
    retail[i] = retail[i].replace('Yes', '1').replace(' (remainder of term)', '').replace('No', '0').replace('Regional', '0.5').replace('Restricted', '0.5').replace(' (districts choice)', '')

lockdown['Schools'] = schools
lockdown['Daycares'] = daycares
lockdown['Bars & sit-down restaurants'] = bars
lockdown['Non-essential retail'] = retail

print(lockdown)

df['SE'] = 0
df['SatH'] = 0
df['OutState'] = 0
df['schools'] = 0
df['daycares'] = 0
df['restaurants'] = 0
df['retail'] = 0

df['Date'] = pd.to_datetime(df.Date)

lockdown.rename(columns = {'State of emergency declared': 'SE', 'Stay at home ordered': 'SatH', 'Out-of-state travel restrictions': 'OutState'}, inplace=True)
lockdown['SE'] = pd.to_datetime(lockdown.SE)
lockdown['SatH'] = pd.to_datetime(lockdown.SatH)

print(lockdown.head)
print(lockdown.shape)

#for i in range(56):
#df.loc[(df['Date'] >= lockdown[''])]
#df.loc[(df['Date'] > '2020-01-25') & (df['state'] == 'Alabama'), 'retail'] = 0
SE = lockdown['SE'].tolist()
state = lockdown['State/territory'].tolist()
schools = lockdown['Schools'].tolist()
daycares = lockdown['Daycares'].tolist()
restaurants = lockdown['Bars & sit-down restaurants'].tolist()
retail = lockdown['Non-essential retail'].tolist()
print(state)
for i in range(len(state)):
    state[i] = state[i].replace(' ', '')
    state[i] = state[i].replace('DistrictofColumbia', 'District of Columbia').replace('NewHampshire', 'New Hampshire').replace('NewJersey', 'New Jersey').replace('NewMexico', 'New Mexico')
    state[i] = state[i].replace('NewMexico', 'New Mexico').replace('NewYork', 'New York').replace('NorthCarolina', 'North Carolina').replace('NorthDakota', 'North Dakota').replace('SouthCarolina', 'South Carolina')
    state[i] = state[i].replace('SouthDakota', 'South Dakota').replace('WestVirginia','West Virginia')
print(state)
for i in range(len(state)):
    df.loc[(df['state'] == state[i]) & (df['Date'] >= SE[i]), 'SE'] = 1
    df.loc[(df['state'] == state[i]) & (df['Date'] >= SE[i]), 'schools'] = float(schools[i])
    df.loc[(df['state'] == state[i]) & (df['Date'] >= SE[i]), 'daycares'] = float(daycares[i])
    df.loc[(df['state'] == state[i]) & (df['Date'] >= SE[i]), 'restaurants'] = float(restaurants[i])
    df.loc[(df['state'] == state[i]) & (df['Date'] >= SE[i]), 'retail'] = float(retail[i])
    print(df[(df['state'] == state[i]) & (df['Date'] >= SE[i])])
home = lockdown['SatH'].tolist()
out = lockdown['OutState'].tolist()

for i in range(len(state)):
    df.loc[(df['state'] == state[i]) & (df['Date'] >= home[i]), 'OutState'] = float(out[i])
    df.loc[(df['state'] == state[i]) & (df['Date'] >= home[i]), 'SatH'] = 1
df.to_excel('Main2.xlsx', engine='xlsxwriter', index = False)