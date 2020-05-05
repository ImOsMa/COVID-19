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
columns.remove('State/territory')
columns.append('Sources')
print(columnsUp)
#print(columnsDown)
print(columns)
df = pd.DataFrame(columns = columns)
val = []

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')
    #print(rows[i])
    #print(len(tds))
    #print(len(columns))
    if len(tds) == len(columns):
        values = [tds[0].text.replace('\n','').replace('Yes', '1').replace('No','0'), tds[1].text.replace('\n','').replace('Yes', '1').replace('No','0'), tds[2].text.replace('\n','').replace('Yes', '1').replace('No','0'), tds[3].text.replace('\n','').replace('Yes', '1').replace('No','0').replace('Mandatory quarantine','2').replace('Travel suspended','2').replace('Limited quarantine','1').replace('Recommended quarantine', '1').replace('Limited quarantine / Screened', '1').replace('Reqional','1').replace('Screened','1'), tds[4].text.replace('\n','').replace('Yes', '1').replace('No','0'), tds[5].text.replace('\n','').replace('Yes', '1').replace('No','0').replace('Restricted','1'), tds[6].text.replace('\n','').replace('Yes', '1').replace('No','0').replace('Restricted','1'), tds[7].text.replace('\n','').replace('Yes','1').replace('No','0').replace('Restricted','1'),tds[8].text.replace('\n','').replace('Yes', '1').replace('No','0').replace('Restricted','1')]
        #print(values)
    else:
        values = [td.text.replace('\n','') for td in tds]
    #print(values)
    if len(tds) > 0:
        df = df.append(pd.Series(values, index = columns), ignore_index = True)
for i in range(2, len(rows)):
    tds = rows[i].find_all('a')
    #print(tds, " - ", i)
    title = tds[0].get('title')
    val.append(title)
print(val)
df.drop('Sources', axis=1, inplace=True)
df['State/territory'] = val
df.to_csv('Quarantine.csv', index=False)
#print(df)
