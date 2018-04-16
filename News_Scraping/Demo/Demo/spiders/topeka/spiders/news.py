import time
import urlparse
import re
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from topeka.items import TopekaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class MySpider(CrawlSpider):
	name = "news"
	start_urls = ["https://www.dropbox.com/news"]
	rules = [Rule(SgmlLinkExtractor(allow=('')), 'parse_news')]

	def parse_news(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.xpath("//div[@class='press-article']")
		items = []
		count = 0
		for titles in titles:
			item = TopekaItem()
			item["initial_url"] = self.start_urls
			item["headline_name"] = titles.xpath("h2/a/text()").extract() or titles.xpath("h3/a/text()").extract()
			item["publish_date"] = (re.search(r'(\d+/\d+/\d+)', str(titles.xpath("p[@class='author']/text()").extract()))).group(1)
			if item["publish_date"]:
				item["date_found"] = "Yes"
			else:
				item["date_found"] = "No"
			item["scanned_date"] = time.strftime("%d/%m/%Y")
			item["url"] = titles.xpath("h2/a/@href").extract() or titles.xpath("h3/a/@href").extract()  or "url"			
			count = count + 1
			for i in item["url"]:
				yield Request(urlparse.urljoin("http:", i), meta={'item': item, 'count': count}, callback=self.parse_body)

	def parse_body(self, response):
		hxss = HtmlXPathSelector(response)
		item = response.request.meta['item']
		count = response.request.meta['count']
		items = []
		temp = 	hxss.xpath("//div[@class='entry']/p/text()").extract() or hxss.xpath("//div[@id='storytext']/p/text()").extract() or hxss.xpath("//div[@class='postBody txtWrap']/p/text()").extract() or hxss.xpath("//div[@id='post-content-331799']/p/text()").extract() or hxss.xpath("//div[@class='body']/p/text()").extract() or hxss.xpath("//div[@class='article-entry text']/p/text()").extract() or hxss.xpath("//div[@class='articleBody']/p/text()").extract() or hxss.xpath("//div[@class='articleBody']/nyt_text/p/text()").extract() or hxss.xpath("//div[@class='main-content']/p/text()").extract() or hxss.xpath("//div[@class='field-item even']/p/text()").extract() or hxss.xpath("//div[@id='article-content']/p/text()").extract() or hxss.xpath("//div[@id='post-body']/p/text()").extract() or hxss.xpath("//div[@class='body prose twelve columns']/p/text()").extract() or hxss.xpath("//section[@class='article-content']/p/text()").extract() or hxss.xpath("//div[@class='post-content']/p/text()").extract() or hxss.xpath("//div[@class='entry-content']/p/text()").extract() or hxss.xpath("//div[@id='articletext']/p/text()").extract() or hxss.xpath("//div[@class='intro-content']/p/text()").extract() or hxss.xpath("//div[@class='maincolumn']/p/text()").extract() or hxss.xpath("//section[@class='entry']/p/text()").extract() or hxss.xpath("//div[@itemprop='articleBody']/p/text()").extract() or hxss.xpath("//span[@name='intellitxt']/p/text()").extract() or hxss.xpath("//bodycopy[@id='bodycopy']/p/text()").extract() or hxss.xpath("//div[@class='txtcontent']/p/text()").extract() or hxss.xpath("//section[@class='page']/p/text()").extract() or hxss.xpath("//p[@class='inside-copy']/text()").extract() or hxss.xpath("//div[@class='entry_body_text']/p/text()").extract() or hxss.xpath("//div[@class='body']/br[8]/text()").extract() or hxss.xpath("//div[@class='body introduction']/p/text()").extract() or hxss.xpath("//div[@class='articlePluckHidden']/p/text()").extract() or hxss.xpath("//div[@class='row post-content']/p/text()").extract() or hxss.xpath("//div[@class='bodyText']/p/text()").extract() or hxss.xpath("//div[@id='article']/p/text()").extract() or hxss.xpath("//section[@class='copy instapaper_body']/p/text()").extract() or hxss.xpath("//div[@id='mod-a-body-after-first-para']/p/text()").extract() or hxss.xpath("//div[@id='article-main']/p/text()").extract() or hxss.xpath("//div[@class='p402_premium']/p/text()").extract() or hxss.xpath("//div[@id='articleBody']/p/text()").extract() or hxss.xpath("//div[@class='body prose twelve columns']/p/text()").extract() or hxss.xpath("//div[@class='content-box']/p/text()").extract() or hxss.xpath("//div[@class='article-body article-text']/p/text()").extract() or hxss.xpath("//div[@class='story-body']/p/text()").extract() or hxss.xpath("//article[@class='w50 ']/p/text()").extract() or hxss.xpath("//div[@class='article']/p/text()").extract() or hxss.xpath("//div[@class='full-body']/p/text()").extract()
		if temp:
			f = open('body_%s_%d.txt' % (self.name, count), 'w+b')
			item["body"] = f.name
		else:
			return
		for i in temp:
			f.write(i.encode('utf-8'))
		items.append(item)
		return items
