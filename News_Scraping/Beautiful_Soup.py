# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 17:51:27 2018
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
@author: narendra_mugada
"""

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
soup = BeautifulSoup(open("news.htm",encoding="utf8"),"html.parser")

print(soup.prettify())

soup.title

soup.title.name

soup.title.string

soup.title.parent.name

soup.p

soup.p['class']

soup.a

soup.find_all('a')

soup.find(id="link3")

#One common task is extracting all the URLs found within a page’s <a> tags:
for link in soup.find_all('a'):
    print(link.get('href'))

print(soup.get_text())

#To get all the links in div tag of class top_nav_cont
for i in soup.find_all('div',{'class':'topnav_cont'}):
    for j in i.find_all('a'):
        print(j.string)

links=[]
for i in soup.find_all('div',{'class':'row_one'}):
    for j in i.find_all('a'):
        print(j.string, j.get('href'))
        
        
        
