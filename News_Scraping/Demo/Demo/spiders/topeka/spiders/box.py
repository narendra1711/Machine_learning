import time
import urlparse
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from topeka.items import TopekaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class BoxSpider(BaseSpider):
	name = "box"
	start_urls = ["https://blog.box.com/category/in-the-news"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.xpath("//div[@class='line mbm']/div")
		count = 1
		for titles in titles:
			item = TopekaItem()
			item["initial_url"] = self.start_urls
			item["headline_name"] = titles.xpath("h3/a/text()").extract()
			item["publish_date"] = titles.xpath("p[@class='small truncate mvs']/text()").extract()			
			if item["publish_date"]:
				item["date_found"] = "Yes"
			else:
				item["date_found"] = "No"
			item["scanned_date"] = time.strftime("%d/%m/%Y")
			item["url"] = titles.xpath("h3/a/@href").extract()
			if item["headline_name"]:
				count = count + 1
			for i in item["url"]:
				yield Request(urlparse.urljoin("http:", i), meta={'item': item, 'count': count}, callback=self.parse_body)

	def parse_body(self, response):
		hxss = HtmlXPathSelector(response)
		item = response.request.meta['item']
		count = response.request.meta['count']
		items = []
		temp = hxss.xpath("//div[@id='article-body']/p/text()").extract() or hxss.xpath("//div[@class='copy post-body']/p[2]/text()").extract() or hxss.xpath("//div[@class='entry']/p/text()").extract() or hxss.xpath("//div[@class='articleBody']/p/text()").extract() or hxss.xpath("//div[@id='section_1']/p/text()").extract() or hxss.xpath("//div[@class='body contains_vestpocket']/p/text()").extract() or hxss.xpath("//div[@id='post-content-721001']/p/text()").extract() or hxss.xpath("//section[@class='body']/p/text()").extract() or hxss.xpath("//div[@class='body yom-art-content clearfix']/p/text()").extract() or hxss.xpath("//div[@id='article_body']/p/text()").extract() or hxss.xpath("//p[@id='deck']/text()").extract() or hxss.xpath("//div[@id='x1213-fey-entroftheyear-rev1']/div[2]/p/text()").extract() or hxss.xpath("//div[@id='post_content']/p/text()").extract()
		if temp:
			f = open('body_%s_%d.txt' % (self.name, count), 'w+b')
			item["body"] = f.name
		else:
			return
		for i in temp:
			f.write(i.encode('utf-8'))
		items.append(item)
		return items
