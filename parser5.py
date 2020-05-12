import csv
import sys
import os
from selenium import webdriver
from time import sleep, time

TABLE = ""
def main():
    driver = webdriver.Chrome()
    driver.get("https://www.worldlifeexpectancy.com/usa/participation-in-physical-activity")
    sleep(5)
    Info = driver.find_elements_by_class_name("highcharts-axis-labels")
    States = Info[2].find_elements_by_tag_name("tspan")
    Info2 = driver.find_elements_by_class_name('highcharts-data-labels')
    Cases = Info2[1].find_elements_by_tag_name("tspan")
    print(len(States))
    print(len(Cases))

    with open("Physical_activity.csv", 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=["State", "Rate Per 100,000"])
        writer.writeheader()
        for i in range(len(States)):
            row = {
                "State": States[i].text,
                "Rate Per 100,000" : Cases[i].text,
            }
            writer.writerow(row)
if __name__ == "__main__":
    main()