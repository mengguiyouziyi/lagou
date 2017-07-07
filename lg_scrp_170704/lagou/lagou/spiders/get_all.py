# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagou.items import LagouItem
import re


class GetAllSpider(CrawlSpider):
	name = 'get_all'
	allowed_domains = ['tianyancha.com']
	start_urls = ['http://www.tianyancha.com/']

	rules = (
		Rule(LinkExtractor(
			allow=r'tianyancha\.com',
		    deny=(r'tianyancha\.com\/search',r'login',r'human',r'company',r'reportContent',
		          r'lawsuit',r'lawfirm', r'property', r'hotnews')),
			follow=True),
		Rule(LinkExtractor(
			allow=(r'tianyancha\.com\/search',),
			deny=(r'login',
			      r'%E5%8C%97%E4%BA%AC%E7%99%BE%E5%BA%A6%E7%BD%91%E8%AE%AF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8')),
			callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		item = LagouItem()
		clist = response.xpath('//a[contains(@class, "query_name")]/@href').extract()
		if clist:
			for c in clist:
				item['id'] = re.search(r'\d+', c).group()
				print(item['id'])
				return item
