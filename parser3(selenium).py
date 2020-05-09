import csv
import sys
import os
from selenium import webdriver
from time import sleep, time

TABLE = ""
def main():
    driver = webdriver.Chrome()
    driver.get("https://www.valuepenguin.com/average-cost-of-health-insurance")
    btn_element = driver.find_elements_by_tag_name("p")
    print(btn_element[3].text)
    sleep(10)
    TABLE = driver.find_element_by_class_name("Table--tbody").find_elements_by_tag_name("tr")
    with open("Insurance_cost.csv", 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=["State", "Monthly cost", "Annual cost", "% change vs. avg."])
        writer.writeheader()
        for tr in TABLE:
            info = tr.find_elements_by_tag_name("td")
            row = {
                "State": info[0].text,
                "Monthly cost": info[1].text,
                "Annual cost": info[2].text,
                "% change vs. avg.": info[3].text,
            }
            writer.writerow(row)
    print("That's all")
if __name__ == "__main__":
    main()