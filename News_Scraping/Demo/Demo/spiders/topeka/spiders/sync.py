import time
import urlparse
import re
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from topeka.items import TopekaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class SyncSpider(BaseSpider):
	name = "sync"
	start_urls = ["http://www.syncplicity.com/about-us/news"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.xpath("//div[@class='record']")
		items = []
		count = 0
		for titles in titles:
			item = TopekaItem()	
			item["initial_url"] = self.start_urls		
			item["headline_name"] = titles.xpath("a/text()").extract()
			item["publish_date"] = (re.search(r'(Jan\ \d+, \d+|Feb\ \d+, \d+|Mar\ \d+, \d+|Apr\ \d+, \d+|May\ \d+, \d+|Jun\ \d+, \d+|Jul\ \d+, \d+|Aug\ \d+, \d+|Sep\ \d+, \d+|Oct\ \d+, \d+|Nov\ \d+, \d+|Dec\ \d+, \d+)', str(titles.xpath("b/text()").extract()))).group(1)
			if item["publish_date"]:
				item["date_found"] = "Yes"
			else:
				item["date_found"] = "No"
			item["scanned_date"] = time.strftime("%d/%m/%Y")
			item["url"] = titles.xpath("a/@href").extract()
			count = count + 1
			for i in item["url"]:
				yield Request(urlparse.urljoin("http:/", i), meta={'item': item, 'count': count}, callback=self.parse_body)

	def parse_body(self, response):
		hxss = HtmlXPathSelector(response)
		item = response.request.meta['item']
		count = response.request.meta['count']
		items = []
		temp = hxss.xpath("//div[@id='article-body']/p/text()").extract() or hxss.xpath("//div[@id='body']/p/text()").extract() or hxss.xpath("//div[@id='post-content-215548']/p/text()").extract() or hxss.xpath("//div[@class='content_box']/p[1]/text()").extract() or hxss.xpath("//div[@id='articleBody']/p/text()").extract() or hxss.xpath("//div[@id='body_content']/p/text()").extract() or hxss.xpath("//div[@id='article-main']/p/text()").extract()
		if temp:
			f = open('body_%s_%d.txt' % (self.name, count), 'w+b')
			item["body"] = f.name
		else:
			return
		for i in temp:
			f.write(i.encode('utf-8'))
		items.append(item)
		return items
