import requests
import time

from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver


class DayForecast(object):
    def __init__(self, day, desc, temp):
        self.day = day
        self.description = desc
        self.temperature = temp

    def __repr__(self):
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


def createForecast(request):
    page = requests.get(request)  # Getting the page from specific URL
    content = BeautifulSoup(page.content, 'html.parser')  # Get the html content
    forecast = content.find(id='seven-day-forecast')
    # Get title
    title = forecast.find(class_='panel-title').get_text()
    # Get days name
    name = forecast.find_all("p", "period-name")
    day_name = [item.get_text() for item in name]
    # Get temperature for each day
    temp = forecast.find_all("p", ["temp temp-high", "temp temp-low"])
    day_temp = [item.get_text() for item in temp]
    # Get description for each day
    desc = forecast.find_all("p", "short-desc")
    day_desc = [item.get_text() for item in desc]

    forcast_days = []
    for i in range(len(day_name)):
        forcast_days.append(DayForecast(day=day_name[i], desc=day_desc[i], temp=day_temp[i]))

    return WeekForecast(forcast_list=forcast_days, title=title)


if __name__ == "__main__":

    address = 'Los Angeles'

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

    # Reading data from the browser and print
    url = browser.current_url
    browser.close()
    week = createForecast(url)
    week.printDay('Today')
    week.printForecast()

