import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

#HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36', 'accept':'*/*'} # для заголовков, будем имитировать работу браузера
URL = 'https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_median_age'

"""
soup = BeautifulSoup(URL, 'lxml')
#print(soup.prettify())
my_table = soup.find('table', {'class':'wikitable sortable'})
l = my_table.findAll('a')
states = []#массив со штатами
for c in l:
    states.append(c.get('title'))
l = my_table.findAll()
"""


article = open('site.html').read()
soup = BeautifulSoup(article, 'html.parser')
my_table = soup.findAll('table', class_='wikitable sortable')

for table in my_table:
    ths = table.findAll('th')
    headings = [th.text.strip() for th in ths]
    if headings[:2] == ['State,'
                        'federal district,'
                        'or territory','Median age'
                                       'in years'
                                       '(Total'
                                       'Population)']:
        break

with open ('data.txt', 'w') as fo:
    for tr in my_table.findAll('tr'):
        tds = tr.findAll('td')
        if not tds:
            continue
        state, age = [td.text.strip() for td in tds[:2]]
        print(', '.join([state,age]), file=fo)
