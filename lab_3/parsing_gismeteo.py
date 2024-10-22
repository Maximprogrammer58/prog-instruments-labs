import re

import csv
import requests


URL = "https://www.gismeteo.ru/diary/4618/2020/9/"
html_page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html_doc = html_page.text

pattern = re.compile(r'<tr align="center">.*?<td class=first>(\d+)</td>.*?<td'
                     r' class=\'first_in_group positive\'>([+-]?\d+)</td>.*?<td>(\d+)</td>.*?<span>'
                     r'<img.*?<br />(.*?)</span>.*?<td class=\'first_in_group positive\'>([+-]?\d+)</td>.*?'
                     r'<td>(\d+)</td>.*?<span><img.*?<br />(.*?)</span>', re.DOTALL)

matches = pattern.findall(html_doc)

with open('weather_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['День', 'Температура', 'Давление', 'Направление ветра', 'Скорость ветра'])
    for match in matches:
        day = match[0]
        temperature = match[1]
        pressure = match[2]
        if match[3]:
            wind = re.findall(r'(\S+)\s+(\d+)', match[3])[0]
            wind_direction, wind_speed = wind[0], wind[1]
        else:
            wind_direction = 'Ш'
            wind_speed = 0
        csv_writer.writerow([day, temperature, pressure, wind_direction, wind_speed])