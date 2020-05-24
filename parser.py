import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import sleep, time
import csv
import sys
import os
from selenium.webdriver.support.ui import WebDriverWait
#Parser


class Parser:

    TABLE = ""
    response = ''
    soup = ''
    rows = ''
    columns = ''
    columnsUp = ''
    DF = ''
    TDS = ''
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'accept': '*/*'}  # для заголовков, будем имитировать работу браузера

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def go_to_page_selenium(self, url):
        self.driver.get(url)

    def go_to_page_bs(self, url):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')


class MedAge(Parser):
    URL = 'https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_median_age'

    def start_parser(self):
        self.go_to_page_bs(self.URL)
        self.finding_table()
        self.filter_table()

    def finding_table(self):
        self.TABLE = self.soup.find('table', {'class': 'wikitable sortable'}).tbody
        self.rows = self.TABLE.find_all('tr')
        self.columns = [v.text.replace('\n', '').replace('[6]', '') for v in self.rows[0].find_all('th')]

    def filter_table(self):
        self.DF = pd.DataFrame(columns=self.columns)

        for i in range(1, len(self.rows)):
            self.TDS = self.rows[i].find_all('td')
            if len(self.TDS) == 3:
                values = [self.TDS[0].text.replace('\n', ''),
                          self.TDS[1].text.replace('\n', '').replace('\xa0', '').replace('[7]', ''),
                          self.TDS[2].text.replace('\n', '')]
            else:
                values = [td.text.replace('\n', '').replace('\xa0', '').replace('[7]', '') for td in self.TDS]
            self.DF = self.DF.append(pd.Series(values, index=self.columns), ignore_index=True)
            self.DF.to_csv('median_age.csv', index=False)


class PopulationDensity(Parser):
    URL = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population_density'

    def start_parse(self):
        self.go_to_page_bs(self.URL)
        self.finding_table()
        self.filter_table()

    def finding_table(self):
        self.TABLE = self.soup.find('table', {'class': 'wikitable sortable mw-collapsible'}).tbody
        self.rows = self.TABLE.find_all('tr')
        self.columnsUp = [v.text.replace('\n', '').replace('[6]', '') for v in self.rows[0].find_all('th')]
        self.columnsUp.remove('Population density')
        self.columnsUp.remove('Population')
        self.columnsUp.remove('Land area')
        self.columns = [v.text.replace('\n', '').replace('[6]', '') for v in self.rows[1].find_all('th')]
        self.columnsUp = self.columnsUp + self.columns

    def filter_table(self):
        self.DF = pd.DataFrame(columns=self.columnsUp)
        for i in range(1, len(self.rows)):
            self.TDS = self.rows[i].find_all('td')

            if len(self.TDS) == 10:
                values = [self.TDS[0].text.replace('\n', '').replace('\xa0', ''),
                          self.TDS[1].text.replace('\n', '').replace('\xa0', '').replace('[7]', ''),
                          self.TDS[2].text.replace('\n', ''), self.TDS[3].text.replace('\n', ''), self.TDS[4].text.replace('\n', ''),
                          self.TDS[5].text.replace('\n', ''), self.TDS[6].text.replace('\n', ''), self.TDS[7].text.replace('\n', ''),
                          self.TDS[8].text.replace('\n', ''), self.TDS[9].text.replace('\n', '')]
            else:
                values = [td.text.replace('\n', '').replace('\xa0', '').replace('[7]', '') for td in self.TDS]
            if values:
                self.DF = self.DF.append(pd.Series(values, index=self.columnsUp), ignore_index=True)

            self.DF.to_csv('population_density.csv', index=False)


class InsuranceCost(Parser):
    URL = "https://www.valuepenguin.com/average-cost-of-health-insurance"

    def start_parse(self):
        self.go_to_page_selenium(self.URL)
        sleep(10)  # one feature
        self.table_work()

    def table_work(self):
        self.TABLE = self.driver.find_element_by_class_name("Table--tbody").find_elements_by_tag_name("tr")
        with open("Insurance_cost.csv", 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["State", "Monthly cost", "Annual cost", "% change vs. avg."])
            writer.writeheader()
            for tr in self.TABLE:
                info = tr.find_elements_by_tag_name("td")
                row = {
                    "State": info[0].text,
                    "Monthly cost": info[1].text,
                    "Annual cost": info[2].text,
                    "% change vs. avg.": info[3].text,
                }
                writer.writerow(row)
        print("That's all")


class StatisticsUsa(Parser):
    URL = "https://www.worldlifeexpectancy.com/usa/heart-disease"
    FILES = ["Heart_Disease.csv","Cancer.csv", "Chronic_Lung.csv", "Diabetes.csv", "Hypertension.csv", "Overweight.csv",
             "Physical_activity.csv", "Pneumonia.csv"]
    PAGES = ["https://www.worldlifeexpectancy.com/usa/cancer", "https://www.worldlifeexpectancy.com/usa/chronic-lung-disease", "https://www.worldlifeexpectancy.com/usa/diabetes",
             "https://www.worldlifeexpectancy.com/usa/hypertension-renal", "https://www.worldlifeexpectancy.com/usa/adult-overweight-obesity-rate",
             "https://www.worldlifeexpectancy.com/usa/participation-in-physical-activity", "https://www.worldlifeexpectancy.com/usa/influenza-pneumonia"]
    s = 0
    states = ''
    cases = ''
    def start_parse(self):
        self.go_to_page_selenium(self.URL)
        sleep(10)
        self.find_table()
        self.collecting_info()

    def find_table(self):
        info = self.driver.find_elements_by_class_name("highcharts-axis-labels")
        self.states = info[2].find_elements_by_tag_name("tspan")
        info2 = self.driver.find_elements_by_class_name('highcharts-data-labels')
        self.cases = info2[1].find_elements_by_tag_name("tspan")

    def collecting_info(self):
        for i in self.FILES:
            self.s += 1
            with open(i, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["State", "Rate Per 100,000"])
                writer.writeheader()
                for k in range(len(self.states)):
                    row = {
                        "State": self.states[k].text,
                        "Rate Per 100,000": self.cases[k].text,
                    }
                    writer.writerow(row)
            self.go_to_page_selenium(self.PAGES[self.s-1])
            sleep(3)
            self.find_table()


class Quarantine(Parser):


