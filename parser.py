import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
""""
def get_html(url,   params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('table', class_='datatableStyles__StyledTable-bwtkle-1 hOnuWY table table-striped')
    #items = soup.find_all('a', href=True)
    #items = soup.find_all('a', href=True)
    print(items)
    country = []
    for item in items:
        pass
def parse():
    html = get_html(URL)
    if (html.status_code) == 200: # status_code делает более читабельный формат
        print('OK')
        get_content(html.text)
    else:
        print('Error')

parse()
class WikiParser(object):

    def parse(self):
        self.go_to_ourtable()
    def go_to_ourtable(self):
        self.driver.get("https://en.wikipedia.org/wiki/List_of_countries_by_median_age")

def main():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/List_of_countries_by_median_age")
    #btn_elem = driver.find_element_by_class_name("/wiki/Afghanistan")
    #btn_elem.click()
    print(name.text)
if __name__ == "__main__":
    main()
"""
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36', 'accept':'*/*'} # для заголовков, будем имитировать работу браузера
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
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class':'wikitable sortable'}).tbody

rows = table.find_all('tr')

columns = [v.text.replace('\n', '').replace('[6]', '') for v in rows[0].find_all('th')]
#print(columns)
df = pd.DataFrame(columns = columns)

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')

    if len(tds) == 3:
        values = [tds[0].text.replace('\n', ''), tds[1].text.replace('\n','').replace('\xa0','').replace('[7]',''), tds[2].text.replace('\n','')]
    else:
        values = [td.text.replace('\n','').replace('\xa0','').replace('[7]','') for td in tds]
    print(values)

    df = df.append(pd.Series(values, index=columns), ignore_index = True)

    df.to_csv('median_age.csv', index=False)
