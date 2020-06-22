import numpy as np
import pandas as pd
import xlrd
import datetime
from itertools import groupby

class CorrectData:
    df = ''
    def __init__(self, MainTable):
        self.MainTableName = MainTable
        self.read_data(self.MainTableName)

    def read_data(self, name):
        self.df = pd.read_csv(name)

    def filter_main_data(self):
        self.df.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Combined_Key', 'Population', 'Case', 'Country/Region'],
                  axis=1, inplace=True)

        cols = self.df.columns.tolist()
        cols = ['Date', 'Province/State', 'Lat', 'Long' ]
        self.df = self.df[cols]

        #удаляем острова и штаты, по которым нет информации
        self.df = self.df.loc[~self.df['Province/State'].isin(['American Samoa'])]
        self.df = self.df.loc[~self.df['Province/State'].isin(['Guam'])]
        self.df = self.df.loc[~self.df['Province/State'].isin(['Puerto Rico'])]
        self.df = self.df.loc[~self.df['Province/State'].isin(['Virgin Islands'])]
        self.df = self.df.loc[~self.df['Province/State'].isin(['Northern Mariana Islands'])]
        self.df = self.df.loc[~self.df['Province/State'].isin(['Grand Princess'])]
        self.df = self.df.loc[~self.df['Province/State'].isin(['Diamond Princess'])]
        #добавляем столбцы
        self.df['positive'] = 0
        self.df['negative'] = 0
        self.df['recovered'] = 0
        self.df['deaths'] = 0
        #удаляем дубликаты и оставляем только первое их вхождение
        self.df = self.df.drop_duplicates(subset=['Date', 'Province/State'], keep='first')

        self.df['Date'] = pd.to_datetime(self.df['Date'])

        self.df.index = np.arange(0, len(self.df))

    def fill_daily_data(self):
        buf  = pd.read_excel('Daily_USA.xlsx')
        self.df['positive'] = buf['positive']
        self.df['negative'] = buf['negative']
        self.df['recovered'] = buf['recovered']
        self.df['deaths'] = buf['deaths']

    def fill_med_age(self):
      buf = pd.read_csv('median_age_states.csv')
      #print(buf)
      state_list = buf["  State"].tolist()
      med_age = buf['  Median age in years (Total Population)'].tolist()
      self.df['med_age'] = 0
      for i in range(len(state_list)):
          self.df.loc[self.df["Province/State"] == state_list[i], "med_age"] = med_age[i]
      #print(self.df.info())

    def fill_lockdowns(self):
        buf = pd.read_csv('Lockdowns.csv')
        buf = buf.drop(['Sources', 'Gatherings banned'], axis=1)

        SED = buf['State of emergency declared'].tolist()
        for i in range(len(SED)):
            SED[i] = SED[i].replace('March ', '2020-03-')
            SED[i] = SED[i].replace('February ', '2020-02-')
            SED[i] = SED[i].replace('January ', '2020-01-')

        SAH = buf['Stay at home ordered'].tolist()
        for i in range(len(SAH)):
            SAH[i] = SAH[i].replace('No','2020-08-01')
            SAH[i] = SAH[i].replace('April ', '2020-04-').replace(' (partial advisory)', '')
            SAH[i] = SAH[i].replace('March ', '2020-03-').replace(' (advisory)', '').replace(' (declared unconstitutional on May 13)', '')
            SAH[i] = SAH[i].replace('February ', '2020-02-')
            SAH[i] = SAH[i].replace('May ', '2020-05-')
            SAH[i] = SAH[i].replace('Regional', '2020-08-01')

        OutTravel = buf['Out-of-state travel restrictions'].tolist()
        for i in range(len(OutTravel)):
            OutTravel[i] = OutTravel[i].replace('No', '0')
            OutTravel[i] = OutTravel[i].replace('Mandatory quarantine',  '2')
            OutTravel[i] = OutTravel[i].replace('Travel suspended', '2')
            OutTravel[i] = OutTravel[i].replace('Limited quarantine', '1').replace(' / Screened', '')
            OutTravel[i] = OutTravel[i].replace('Recommended quarantine', '1').replace(' / Screened', '')
            OutTravel[i] = OutTravel[i].replace('Regional', '1').replace(' / Screened', '')
            OutTravel[i] = OutTravel[i].replace('Screened', '1')

        schools = buf['Schools'].tolist()
        daycare = buf['Daycares'].tolist()
        rest = buf['Bars & sit-down restaurants'].tolist()
        retail = buf['Non-essential retail'].tolist()

        for i in range(len(schools)):
            schools[i] = schools[i].replace('Yes', '1').replace('(remainder of term)', '').replace('No', '0').replace('Restricted', '0.5').replace('Regional', '0.5').replace(' (districts choice)', '').replace(' ', '')
            daycare[i] = daycare[i].replace('Yes', '1').replace('(remainder of term)', '').replace('No', '0').replace('Restricted', '0.5').replace('Regional', '0.5').replace(' (districts choice)', '').replace(' ', '')
            rest[i] = rest[i].replace('Yes', '1').replace('(remainder of term)', '').replace('No', '0').replace('Restricted', '0.5').replace('Regional', '0.5').replace(' (districts choice)', '').replace(' ', '')
            retail[i] = retail[i].replace('Yes', '1').replace('(remainder of term)', '').replace('No', '0').replace('Restricted', '0.5').replace('Regional', '0.5').replace(' (districts choice)', '').replace(' ', '')

        self.df['SED'] = 0
        self.df['SAH'] = 0
        self.df['OutS'] = 0
        self.df['schools'] = 0
        self.df['daycare'] = 0
        self.df['rest'] = 0
        self.df['retail'] = 0

        state_list = buf['State/territory'].tolist()

        buf['State of emergency declared'] = SED
        buf['Stay at home ordered'] = SAH
        buf['OutS'] = OutTravel
        buf['State of emergency declared'] = pd.to_datetime(buf['State of emergency declared'])
        buf['Stay at home ordered'] = pd.to_datetime(buf['Stay at home ordered'])

        SED = buf['State of emergency declared'].tolist()
        SAH = buf['Stay at home ordered'].tolist()

        for i in range(len(state_list)):
            state_list[i] = state_list[i].replace(' ', '')
            state_list[i] = state_list[i].replace('DistrictofColumbia','District of Columbia')
            state_list[i] = state_list[i].replace('NewHampshire', 'New Hampshire')
            state_list[i] = state_list[i].replace('NewJersey', 'New Jersey')
            state_list[i] = state_list[i].replace('NewMexico', 'New Mexico')
            state_list[i] = state_list[i].replace('NewYork', 'New York')
            state_list[i] = state_list[i].replace('NorthCarolina', 'North Carolina')
            state_list[i] = state_list[i].replace('NorthDakota', 'North Dakota')
            state_list[i] = state_list[i].replace('SouthCarolina','South Carolina')
            state_list[i] = state_list[i].replace('SouthDakota', 'South Dakota')
            state_list[i] = state_list[i].replace('WestVirginia', 'West Virginia')

        print(len(SED))
        S = self.df['Date'].tolist()
        S = S[:125]
        print(S)
        for i in range(len(state_list)):
           self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date']>=SED[i]), "SED"] = 1
           self.df.loc[(self.df["Province/State"] == state_list[i])& (self.df['Date']>=SED[i]), "schools"] = float(schools[i])
           self.df.loc[(self.df["Province/State"] == state_list[i])& (self.df['Date']>=SED[i]), "daycare"] = float(daycare[i])
           self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date']>=SED[i]), "rest"] = float(rest[i])
           self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date']>=SED[i]), "retail"] = float(retail[i])

        for i in range(len(state_list)):
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= SAH[i]), "SAH"] = 1
            self.df.loc[(self.df["Province/State"] == state_list[i])& (self.df['Date'] >= SAH[i]), "OutS"] = int(OutTravel[i])

    def fill_open(self):
        buf = pd.read_csv('Open.csv')
        buf = buf.drop(['Date enacted'], axis=1)
        dates = buf['Date lifted'].tolist()

        for i in range(len(dates)):
            dates[i] = dates[i].replace('April ', '2020-04-')
            dates[i] = dates[i].replace('May ', '2020-05-')
            dates[i] = dates[i].replace(' ', '')

        buf['Date lifted'] = dates
        buf['Date lifted'] = pd.to_datetime(buf['Date lifted'])

        dates = buf['Date lifted'].tolist()
        state_list = buf['State'].tolist()
        S = self.df['Date'].tolist()

        for i in range(len(state_list)):
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "SED"] = 0
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "schools"] = 0
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "daycare"] = 0
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "rest"] = 0
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "retail"] = 0
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "SAH"] = 0
            self.df.loc[(self.df["Province/State"] == state_list[i]) & (self.df['Date'] >= dates[i]), "OutS"] = 0


    def fill_population(self):
        buf = pd.read_csv('population_density.csv', delimiter = ',')
        buf = buf.drop(['Rank(all)', 'Rank(50 states)', 'permi2', 'Rank', 'Rank.1', 'mi2'], axis=1)
        per = buf['perkm2'].tolist()
        state_list = buf['State etc.'].tolist()
        num = buf['Numbers'].tolist()

        for i in range(len(per)):
            per[i] = per[i].replace('<', '')
            per[i] = int(per[i])
            num[i] = int(num[i].replace('.', ''))

        self.df['pop_density'] = 0
        self.df['pop_num'] = 0
        for i in range(len(state_list)):
            self.df.loc[(self.df["Province/State"] == state_list[i]), "pop_density"] = per[i]
            self.df.loc[(self.df["Province/State"] == state_list[i]), "pop_num"] = num[i]

    def fill_insurance(self):
        buf = pd.read_csv('Insurance_cost.csv')
        buf = buf.drop(['Annual cost', '% change vs. avg.'], axis=1)
        cost = buf['Monthly cost'].tolist()
        state_list = buf['State'].tolist()

        self.df['insurance'] = 0

        for i in range(len(cost)):
            cost[i] = int(cost[i].replace('$', ''))
        for i in range(len(state_list)):
            self.df.loc[(self.df["Province/State"] == state_list[i]), "insurance"] = cost[i]


    def fill_diseases(self):
        buf = pd.read_excel('Common_Table_Deases.xlsx')
        state_list = buf['State'].tolist()
        pneu = buf['Pneumonia'].tolist()
        pact = buf['Physcial activity'].tolist()
        over = buf['Overweight'].tolist()
        hyper = buf['Hypertension'].tolist()
        heart = buf['Heart_Deasese'].tolist()
        dia = buf['Diabets'].tolist()
        lung = buf['Chronic_Lung'].tolist()
        can = buf['Canser'].tolist()

        self.df['pneumonia'] = 0
        self.df['activity'] = 0
        self.df['overweight'] = 0
        self.df['hypertension'] = 0
        self.df['heart'] = 0
        self.df['diabets'] = 0
        self.df['lung'] = 0
        self.df['cancer'] = 0

        for i in range(len(state_list)):
            state_list[i] = state_list[i].replace(' ', '')
            state_list[i] = state_list[i].replace('DistrictofColumbia','District of Columbia')
            state_list[i] = state_list[i].replace('NewHampshire', 'New Hampshire')
            state_list[i] = state_list[i].replace('NewJersey', 'New Jersey')
            state_list[i] = state_list[i].replace('NewMexico', 'New Mexico')
            state_list[i] = state_list[i].replace('NewYork', 'New York')
            state_list[i] = state_list[i].replace('NorthCarolina', 'North Carolina')
            state_list[i] = state_list[i].replace('NorthDakota', 'North Dakota')
            state_list[i] = state_list[i].replace('SouthCarolina','South Carolina')
            state_list[i] = state_list[i].replace('SouthDakota', 'South Dakota')
            state_list[i] = state_list[i].replace('WestVirginia', 'West Virginia')


        for i in range(len(state_list)):
            self.df.loc[(self.df["Province/State"] == state_list[i]), "pneumonia"] = float(pneu[i])
            self.df.loc[(self.df["Province/State"] == state_list[i]), "activity"] = float(pact[i].replace('%', ''))
            self.df.loc[(self.df["Province/State"] == state_list[i]), "overweight"] = float(over[i].replace('%',''))
            self.df.loc[(self.df["Province/State"] == state_list[i]), "hypertension"] = float(hyper[i])
            self.df.loc[(self.df["Province/State"] == state_list[i]), "heart"]  = float(heart[i])
            self.df.loc[(self.df["Province/State"] == state_list[i]), "diabets"]  = float(dia[i])
            self.df.loc[(self.df["Province/State"] == state_list[i]), "lung"] = float(lung[i])
            self.df.loc[(self.df["Province/State"] == state_list[i]), "cancer"] = float(can[i])

    def correct_data(self):
        self.df['negative'].fillna(0.0, inplace=True)
        writer = pd.ExcelWriter('Data.xlsx', engine='xlsxwriter')
        self.df.to_excel(writer, 'Sheet1')
        writer.save()







t = CorrectData('USA.csv')
t.filter_main_data()
t.fill_daily_data()
t.fill_med_age()
t.fill_lockdowns()
t.fill_open()
t.fill_population()
t.fill_insurance()
t.fill_diseases()
t.correct_data()