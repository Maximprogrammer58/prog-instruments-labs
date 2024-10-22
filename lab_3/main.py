import re
import requests


URL = "https://www.gismeteo.ru/diary/4618/2020/9/"
html_page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html_doc = html_page.text

pattern = re.compile(r'<tr align="center">.*?<td class=first>(\d+)</td>.*?<td'
                     r' class=\'first_in_group positive\'>([+-]?\d+)</td>.*?<td>(\d+)</td>.*?<span>'
                     r'<img.*?<br />(.*?)</span>.*?<td class=\'first_in_group positive\'>([+-]?\d+)</td>.*?'
                     r'<td>(\d+)</td>.*?<span><img.*?<br />(.*?)</span>', re.DOTALL)

matches = pattern.findall(html_doc)
print(matches)