import csv
import datetime


def read_data(path: str) -> list:
    """Getting data from a file
    Args:
      path: the path to the file for reading information
    Returns:
      list of days with weather information
    """
    data = []
    with open(path, "r", encoding="utf-8") as file:
        for line in csv.reader(file):
            data.append(line)
    return data


def growth(today: str, next_day: str) -> int:
    """
    Args:
      today: the date of today
      next_day: the date of the next day
    Returns:
      The number of days between them (the difference between the days)
    """
    current_day = datetime.datetime.strptime(today, '%Y-%m-%d').date()
    following_day = datetime.datetime.strptime(next_day, '%Y-%m-%d').date()
    return (following_day - current_day).days