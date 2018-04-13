# -*- coding: utf-8 -*-
import scrapy

class NdtvscrapingSpider(scrapy.Spider):
    name = 'NDTVScraping'
    allowed_domains = ['https://www.ndtv.com/tamil-nadu-news/cauvery-protests-live-updates-tamil-outfit-protests-outside-ipl-venue-in-chennai-1835541']
    start_urls = ['https://www.ndtv.com/tamil-nadu-news/cauvery-protests-live-updates-tamil-outfit-protests-outside-ipl-venue-in-chennai-1835541/']

    def parse(self, response):
        t=response.css(".ins_descp::text").extract()
        d=response.css(".ins_storybody::text").extract()
        m=response.css(".ins_mainimage_big story_pic::text").extract()
        dict={}
        for item in zip(t,d,m):
            dict={
                    'Title':item[0],
                    'Data':item[1],
                    'Main Data':item[2],
                    }
            
        yield(dict)
        
