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