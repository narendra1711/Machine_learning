# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 20:58:36 2018

@author: narendra
"""

import scrapy

class Flipkart_Scraping:
    name="flipkartbot"
    allowed_domains=["https://www.flipkart.com/"]
    def parse(self,response):
        #extraction
        phones=response.css("._3wU53n::text").extract()
        #extract data in rowise
        for phone in phones:
            #add to dict
            scraped_info={
                    'phone':phone[0]}
        yield(scraped_info)