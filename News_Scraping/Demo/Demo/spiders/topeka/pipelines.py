# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem

class TopekaPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('item.csv', 'a+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        with open('item.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            data = []
            for row in reader:
                content = row[0]
                data.append(content)
        if item["body"] in data:
            file = open('duplicate item.csv', 'a+b')
            self.files[spider] = file
            self.exporter = CsvItemExporter(file)
            self.exporter.start_exporting()
            self.exporter.export_item(item)
            return item
        else:
            self.exporter.export_item(item)
            return item
