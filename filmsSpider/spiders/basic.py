# -*- coding: utf-8 -*-
import scrapy
import datetime
from urllib.parse import urljoin
from filmsSpider.items import FilmItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import re
from scrapy.http import Request

class BasicSpider(scrapy.Spider):
	name = 'basic'
	allowed_domains = ['www.bbc.co.uk']
	start_urls = ['https://www.bbc.co.uk/iplayer/categories/films/all?sort=atoz']

	def parse(self, response):
		next_link = response.css('.next.txt a::attr(href)').extract_first()
		if next_link is not None:
			yield Request(urljoin(response.url, next_link))

		series_selector = response.css('.programme .view-more-grid a.avail::attr(href)')
		for seriesUrl in series_selector.extract():
			yield Request(urljoin(response.url, seriesUrl))

		selectors = response.css(".programme, .episode")
		for selector in selectors:
			yield self.parse_item(selector, response)

	def parse_item(self, selector, response):
		l = ItemLoader(item=FilmItem(), selector=selector)
		l.add_css('title', '.top-title::text')
		l.add_css('subtitle', '.subtitle::text')
		l.add_css('synopsis', '.synopsis::text')
		l.add_css('duration', '.duration::text', MapCompose(self.parse_duration))

		item_link = response.css('a.list-item-link::attr(href)').extract_first()
		if item_link is not None:
			yield Request(urljoin(response.url, item_link))

		# housekeeping
		l.add_css('url', 'a.list-item-link::attr(href)', MapCompose(lambda i: urljoin(response.url, i)))
		l.add_value('date', datetime.datetime.now())

		return l.load_item()

	def parse_duration(self, s):
		matches = re.search('([0-9]+)', s)
		if matches is not None:
			return int(matches.group(0))
