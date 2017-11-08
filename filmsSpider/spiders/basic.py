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
		title = selector.css('.title::text').extract_first()
		subtitle = selector.css('.subtitle::text').extract_first()
		synopsis = selector.css('.synopsis::text').extract_first()
		m = MapCompose(self.parse_duration)
		duration = m(selector.css('.duration::text').extract())[0],

		item_link = selector.css('a.list-item-link::attr(href)').extract_first()
		# self.log("link %s" % urljoin(response.url, item_link));
		if item_link is not None:
			return Request(urljoin(response.url, item_link), callback=self.parse_page, meta={
				'URL': urljoin(response.url, item_link),
				'title': title,
				'subtitle': subtitle,
				'synopsis' : synopsis,
				'duration': duration
				})
		else:
			return None;

	def parse_page(self, response):
		url = response.meta.get('URL')
		l = ItemLoader(item=FilmItem())

		l.add_value('title', response.meta.get('title'))
		l.add_value('subtitle', response.meta.get('subtitle'))
		l.add_value('synopsis', response.meta.get('synopsis'))
		l.add_value('duration', response.meta.get('duration'))

		# housekeeping
		l.add_value('url', url)
		l.add_value('date', datetime.datetime.now())

		yield l.load_item()

	def parse_duration(self, s):
		matches = re.search('([0-9]+)', s)
		if matches is not None:
			return int(matches.group(0))
