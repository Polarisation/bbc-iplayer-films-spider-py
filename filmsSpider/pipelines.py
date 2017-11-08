# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class FilmsspiderPipeline(object):
	def process_item(self, item, spider):
		return item

class DuplicatesPipeline(object):
	def __init__(self):
		self.urls_seen = set()

	def process_item(self, item, spider):
		if item['url'][0] in self.urls_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.urls_seen.add(item['url'][0])
			return item
