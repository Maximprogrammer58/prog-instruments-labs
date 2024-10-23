import re
import requests

from file_handler import write_csv, read_logs


def parsing_weather() -> None:
    URL = "https://www.gismeteo.ru/diary/4618/2020/9/"
    html_page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    html_doc = html_page.text
    data = []

    pattern = re.compile(r'<tr align="center">.*?<td class=first>(\d+)</td>.*?<td'
                         r' class=\'first_in_group positive\'>([+-]?\d+)</td>.*?<td>(\d+)</td>.*?<span>'
                         r'<img.*?<br />(.*?)</span>.*?<td class=\'first_in_group positive\'>([+-]?\d+)</td>.*?'
                         r'<td>(\d+)</td>.*?<span><img.*?<br />(.*?)</span>', re.DOTALL)

    matches = pattern.findall(html_doc)

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
        data.append([day, temperature, pressure, wind_direction, wind_speed])

    write_csv('parsing_weather', data, ["День", "Температура", "Давление", "Направление ветра", "Скорость ветра"])


def parsing_logs(logs_path: str):
    logs = read_logs(logs_path)
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (?P<level>\w+)\s+(?P<source>\w+)\s+(?P<message>.*)'
    matches = re.findall(pattern, logs)
    write_csv("parsing_logs", matches, ['Timestamp', 'Level', 'Source', 'Message'])




