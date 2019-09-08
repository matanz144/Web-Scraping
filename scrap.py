# This file is just for learning and try new things,
# The code in this file probably won't work

import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = 'https://forecast.weather.gov/MapClick.php?lat=40.7145&lon=-74.006#.XXTS4igzaUk'



if __name__ == "__main__":
    page = requests.get(URL)  # Getting the page from specific URL
    content = BeautifulSoup(page.content, 'html.parser')  # Get the html content
    week = content.find(id='seven-day-forecast')
    tag_li = week.find_all(class_='forecast-tombstone')
    # Get days name
    name = week.find_all("p", "period-name")
    day_name = [item.get_text() for item in name]
    # Get tempature for each day
    temp = week.find_all("p", ["temp temp-high", "temp temp-low"])
    day_temp = [item.get_text() for item in temp]
    # Get description for each day
    desc = week.find_all("p", "short-desc")
    day_desc = [item.get_text() for item in desc]
    forecast = []
    for i in range(len(temp)):
        forecast.append({'Day': day_name[i], 'Temp': day_temp[i], 'Description': day_desc[i]})

    # pprint(title)
    print(forecast)
    # print(day_name)
    # print(day_temp)


