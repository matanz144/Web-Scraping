import requests
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup


class DayForecast(object):
    def __init__(self, day, desc, temp):
        self.day = day
        self.description = desc
        self.temperature = temp

    def __repr__(self):
        return 'Day: {}, Dsecription: {}, Temperature: {}'.format(self.day, self.description, self.temperature)


class WeekForecast(DayForecast):
    def __init__(self, forcast_list, title):
        self.week: DayForecast = forcast_list
        self.title = title

    def __repr__(self):
        return 'Title: {}, Week_Forecast: {}'.format(self.title, pprint(self.week))

def createForecast(request):

    page = requests.get(request)
    soup = BeautifulSoup(page.content, 'html.parser')
    week = soup.find(id='seven-day-forecast-body')
    items = week.find_all(class_='tombstone-container')
    title = soup.find(class_='panel-title').get_text()
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
    site = 'https://forecast.weather.gov/MapClick.php?lat=34.05349000000007&lon=-118.24531999999999#.XUfvWegzaUk'
    week = createForecast(site)
    print(week)



