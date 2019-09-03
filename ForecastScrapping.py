import requests
import pandas as pd
import time
import sys

from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DRIVER_PATH = 'c/Users/pmmatan/PycharmProjects/WebScrappingLearning/chromedriver.exe'


class DayForecast(object):
    def __init__(self, day, desc, temp):
        self.day = day
        self.description = desc
        self.temperature = temp

    def __repr__(self):
        # return repr(dict(Day=self.day, Dsecription=self.description, Temperature=self.temperature))
        return 'Day: {}, Dsecription: {}, Temperature: {}'.format(self.day, self.description, self.temperature)


class WeekForecast(DayForecast):
    def __init__(self, forcast_list, title):
        self.day: DayForecast = forcast_list
        self.title = title

    def __repr__(self):
        return 'Title: {}, Week_Forecast: {}'.format(self.title, self.day)

    def printForecast(self):
        print(self.title)
        for day in self.day:
            print(day)

    def printDay(self, day):
        print('{} -- {}'.format(self.title, day))
        for item in self.day:
            i = self.day.index(item)
            if day == item.day:
                print(self.day[i])
                print(self.day[i + 1])
        # print(self.title, day)




def createForecast(request, title):
    page = requests.get(request)
    soup = BeautifulSoup(page.content, 'html.parser')
    week = soup.find(id='seven-day-forecast-body')
    items = week.find_all(class_='tombstone-container')
    # title = soup.find_all(class_='panel-title')
    # title2 = soup.find(class_='panel-title').get_text()
    days = [item.find(class_='period-name').get_text() for item in items]  # Get a list of all days
    description = [item.find(class_='short-desc').get_text() for item in items]  # Get description for each day
    temperature = getTemp(items=items)  # Get a list of temperature for each day
    forcast_days = []
    for i, item in enumerate(items):
        day = DayForecast(day=days[i], desc=description[i], temp=temperature[i])
        forcast_days.append(day)
        # forcast.forcast_list.append(day)

    # pprint(forcast_days)
    return WeekForecast(forcast_list=forcast_days, title=title)


def getTemp(items):
    temp_list = []
    for item in items:
        if items.index(item) % 2 == 0:
            temp_list.append(item.find(class_='temp temp-high').get_text())
        else:
            temp_list.append(item.find(class_='temp temp-low').get_text())
    return temp_list


if __name__ == "__main__":
    # address = ''.join(sys.argv[1:])
    address = 'Manhatten'

    site = 'https://forecast.weather.gov/MapClick.php?lat=40.71455000000003&lon=-74.00713999999994#.XW5KLSgzaUk'
    # week = createForecast(site, address)
    # week.printForecast()


    # Create and open a new session in Firefox
    browser = webdriver.Firefox()
    browser.get('https://weather.gov')

    # Define and make the search
    search_box = browser.find_element_by_id('inputstring')
    go_btn = browser.find_element_by_id('btnSearch')
    search_box.clear()
    search_box.send_keys(address)
    time.sleep(2)
    go_btn.click()
    browser.implicitly_wait(15)

    # Reading data from the browser and print
    url = browser.current_url
    week = createForecast(site, address)
    week.printDay('Today')
    # week.printForecast()

