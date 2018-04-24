# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:19:33 2018

@author: narendra_mugada
"""

import feedparser as fp

url="http://rss.cnn.com/rss/edition.rss"

def parse(url):
    return fp.parse(url)

def getsource(parsed):
    feed=parsed['feed']
    return {
            'link':feed['link'],
            'title':feed['title'],
            'subtitle':feed['subtitle']}
    
def getarticles(parsed):
    articles=[]
    entries=parsed['entries']
    for entry in entries:
        articles.append({
                'id':entry['id'],
                'link':entry['link'],
                'title':entry['title'],
                'published':entry['published']})
        return articles
    
parsed=parse(url)

getsource(parsed)

getarticles(parsed)