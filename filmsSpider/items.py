# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class FilmItem(scrapy.Item):
	# primary fields
	title = Field();
	subtitle = Field();
	synopsis = Field();
	duration = Field();
	description = Field();

	# housekeeping fields
	url = Field();
	date = Field();
