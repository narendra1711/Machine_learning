from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import Crawler
import csv
import re
import time
from topeka.spiders.news import MySpider
from topeka.spiders.box import BoxSpider
from topeka.spiders.sync import SyncSpider
from topeka.spiders.syncpress import SyncpSpider

def item_count():
	reader = csv.reader(open('item.csv', 'rb'))
	reader1 = csv.reader(open('keywords.csv', 'rb'))
	writer = csv.writer(open('plot_data.csv', 'a+b'))
	reader2 = csv.reader(open('plot_data.csv', 'rb'))
	
	data1 = ["Week"]
	data2 = []
	for row1 in reader1:
		data1.extend(row1)
		data2.extend(row1)
	data3 = []
	for row in reader2:
		data3.extend(row)
		break
	if len(data3) == 0:
		writer.writerow(data1)
	
	contentlist = []
	j = time.strftime("%U")
	repetdict = ["Week "+j]
	contentlist1 = []
	for row in reader:
		content = re.search(r'(\w+.txt)', str(row[0]))
		if content:
			body_reader = open(content.group(1), 'rb')
			body_reader_temp = body_reader.read()
			contentlist = body_reader_temp.split()
			contentlist1.append(contentlist)
	
	for i in data2:
		count = 0
		for item in contentlist1:
			for words in item:
				if words == i:
					count = count + 1
		repetdict.append(count)
	if repetdict:
		writer.writerow(repetdict)

def post_processing():
	reader = csv.reader(open('item.csv', 'rb'))
	reader1 = csv.reader(open('keywords.csv', 'rb'))
	writer = csv.writer(open('output1.csv', 'w+b'))
	data1 = []
	for row1 in reader1:
		row2 = row1[0]
		data1.append(row2)
	data2 = []
	for row in reader:
		content = re.search(r'(\w+.txt)', str(row[0]))
		if content:
			body_reader = open(content.group(1), 'rb')
			body_reader_temp = body_reader.read()
			for i in data1:
				if i in body_reader_temp:
					temp = "True"
					data2.append(temp)
				else:
					temp = "False"
					data2.append(temp)
			writer.writerow(row + data2)
			data2 = []
		else:
			writer.writerow(row + data1)

def setup_crawler(domain):
	spider = domain()
	settings = get_project_settings()
	crawler = Crawler(settings)
	if domain == MySpider:
		crawler.signals.connect(reactor.stop, signal=signals.spider_closd)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()

# Usage 
if __name__ == "__main__": 
	log.start()
	for domain in [MySpider, BoxSpider, SyncSpider, SyncpSpider]:
		setup_crawler(domain)
	reactor.run()
	post_processing()
	item_count()
