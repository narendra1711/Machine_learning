# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 19:36:03 2018

@author: narendra
"""

from bs4 import BeautifulSoup
import requests, re
import pandas as pd

page = 'http://www.bbc.com/news'
open_page = requests.get(page).text
soup = BeautifulSoup(open_page, 'lxml')

recent_news = soup.find('div', attrs={'class': 'gel-wrap gs-u-pt+'})

articles = recent_news(['h3', 'time'])
time_pattern = r'^[0-9]{1,2}[h,m]{1}'

print('Most recent news:')
for article in articles:
    print(re.sub(time_pattern, '', article.text))