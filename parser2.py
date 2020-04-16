import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

URL = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population_density'
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class':'wikitable sortable mw-collapsible'}).tbody

rows = table.find_all('tr')
columnsUp = [v.text.replace('\n', '').replace('[6]', '') for v in rows[0].find_all('th')]
columnsUp.remove('Population density')
columnsUp.remove('Population')
columnsUp.remove('Land area')
columns = [v.text.replace('\n', '').replace('[6]', '') for v in rows[1].find_all('th')]
columnsUp = columnsUp + columns
print(columnsUp)
df = pd.DataFrame(columns = columnsUp)

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')

    if len(tds) == 10:
        values = [tds[0].text.replace('\n', '').replace('\xa0',''), tds[1].text.replace('\n','').replace('\xa0','').replace('[7]',''), tds[2].text.replace('\n',''), tds[3].text.replace('\n',''), tds[4].text.replace('\n',''), tds[5].text.replace('\n',''), tds[6].text.replace('\n',''), tds[7].text.replace('\n',''), tds[8].text.replace('\n',''), tds[9].text.replace('\n','')]
    else:
        values = [td.text.replace('\n','').replace('\xa0','').replace('[7]','') for td in tds]
    print(values)
    if values:
      df = df.append(pd.Series(values, index=columnsUp), ignore_index = True)

    df.to_csv('population_density.csv', index=False)
