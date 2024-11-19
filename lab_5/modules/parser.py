import csv
import requests

from bs4 import BeautifulSoup


def correct_wind_info(wind: str) -> tuple:
    """Separation of wind direction and speed data by variables
    Args:
      wind: wind information
    Returns:
      A tuple with wind speed and direction
    """
    direction, speed = wind.split()
    digit_speed = int(''.join(filter(str.isdigit, speed)))
    return direction, digit_speed


def parser(year_from: int, year_to: int, step=1) -> list:
    """Parsing data from the site by url and further adding data to the list
    Args:
      year_from: year of the beginning of parsing
      year_to: year of parsing completion
      step: step for years
    Returns:
      List of days received as a result of parsing
    Raises:
      Exception: information for the current day is not available on the website
    """
    parser_data = []
    for year in range(year_from, year_to + 1, step):
        for month in range(1, 13):
            URL = f"https://www.gismeteo.ru/diary/4618/{year}/{month}/"
            html_page = requests.get(
                URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(html_page.text, 'lxml')
            for day in soup.find_all('td', class_="first"):
                try:
                    temp = day.find_next()
                    press = temp.find_next()
                    wind = press.find_next_sibling().find_next_sibling().find_next_sibling()
                    durection, digit_speed = correct_wind_info(wind.text)
                    parser_data.append([str(year) + "-" + str(month).zfill(2) + "-" + day.text.zfill(2),
                                        int(temp.text), press.text, durection, digit_speed])
                except:
                    pass
    return parser_data


def upload_csv(parser_data: list) -> None:
    """Saving data after parsing to a csv file
    Args:
      parser_data: list of days received as a result of parsing
    """
    with open('dataset.csv', 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(parser_data)

