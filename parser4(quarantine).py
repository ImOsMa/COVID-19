import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

URL = 'https://en.wikipedia.org/wiki/U.S._state_and_local_government_response_to_the_2020_coronavirus_pandemic'
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table',{'class':'wikitable sortable'}).tbody

rows = table.find_all('tr')
columnsUp = [v.text.replace('\n', '') for v in rows[0].find_all('th')]
columnsDown = [v.text.replace('\n', '') for v in rows[1].find_all('th')]
columnsUp.remove('Closures ordered')
columnsUp.remove('Sources')
columns = columnsUp + columnsDown
#print(columnsUp)
#print(columnsDown)
print(columns)
df = pd.DataFrame(columns = columns)

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')

    if len(tds) == len(columns):
        values = [tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text]

    else:
        values = [td.text for td in tds]
    print(values)
    if values:
        df = df.append(pd.Series(values, index = columns), ignore_index=True)