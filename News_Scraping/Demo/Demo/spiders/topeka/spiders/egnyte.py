from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from topeka.items import TopekaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class MySpider(CrawlSpider):
	name = "news"
	allowed_domains = ["egnyte.com"]
	start_urls = ["http://egnyte.com/corp/egnyte-file-storage-news.html"]
	rules = [Rule(SgmlLinkExtractor(allow=('/corp/egnyte-file-storage-news.html')), 'parse_news')]

	def parse_news(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select("//div[@id='bookcontent']")
		items = []
		for titles in titles:
			item = TopekaItem()
			item["extracted_url"] = titles.select("a/@href").extract()
			item["headline_name"] = titles.select("a/text()").extract()
			item["publish_date"] = titles.select("br/text()").extract()
			items.append(item)
		return items