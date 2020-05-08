import csv
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36', 'accept':'*/*'} # для заголовков, будем имитировать работу браузера
URL = 'https://www.valuepenguin.com/average-cost-of-health-insurance'

class Parser:
    TABLE = ""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
    def go_to_taget_page(self, url):
        self.driver.get(url)
    def go_to_main_page(self):
        self.driver.get(URL)
class ParseInsurance(Parser):
    OurUrl = "https://www.valuepenguin.com/average-cost-of-health-insurance"

    def __init__(self, driver):
        super().__init__(driver)
    def start_parse(self):
        self.go_to_taget_page(self.OurUrl)
        self.find_main_table()
        self.collecting_information_from_table()
    def find_main_table(self):
        sleep(3)
        self.TABLE = self.driver.find_element_by_class_name("Table--tbody").find_elements_by_tag_name("tr")
    def collecting_information_from_table(self):
        with open("Insurance_cost.csv", 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["State", "Monthly cost", "Annual cost", "% change vs. avg."])
            writer.writeheader()
            #scraping

            for tr in self.TABLE:
                info = tr.find_elements_by_tag_name("td")
