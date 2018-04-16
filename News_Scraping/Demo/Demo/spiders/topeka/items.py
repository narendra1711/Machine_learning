# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TopekaItem(Item):
	initial_url = Field()
	url =Field()
	publish_date = Field()
	scanned_date = Field()	
	headline_name = Field()
	body = Field()
	date_found = Field()
