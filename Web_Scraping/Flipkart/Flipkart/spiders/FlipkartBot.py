# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class FlipkartbotSpider(scrapy.Spider):
    name = 'FlipkartBot'
    allow_urls=['https://www.flipkart.com/search?q=iphone&otracker=start&as-show=on&as=off/']
    start_urls = ['https://www.flipkart.com/search?q=iphone&otracker=start&as-show=on&as=off/']
    
    def parse(self, response):
        Phone_Model=response.css("._3wU53n::text").extract()
        Price=response.css("._1vC4OE _2rQ-NK::text").extract()
        dict={}
        for items in zip(Phone_Model,Price):
            dict={
                    "Model":items[0],
                    "Cost":items[1],}
                    
        yield(dict)