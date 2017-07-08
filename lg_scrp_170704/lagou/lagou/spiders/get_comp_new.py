# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from lagou.items import LagouItem
from lagou.utils.mysql2redis import get_id


class GetAllSpider(Spider):
	name = 'get_comp_new'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/gongsi/{lg_comp_id}.html'
	custom_settings = {
		'DOWNLOADER_MIDDLEWARES': {
			'lagou.middlewares.ProxyMiddleware': 1,
			'lagou.middlewares.RedirctMiddleware': 110,
			'lagou.middlewares.RotateUserAgentMiddleware': 2,
		},
		'DEFAULT_REQUEST_HEADERS': {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			"Referer": "https://www.lagou.com/jobs/list_%E7%99%BE%E5%BA%A6?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords&suginput=",
			'Accept-Encoding': "gzip, deflate, br",
			'Upgrade-Insecure-Requests': "1",
			# 'X-Anit-Forge-Code': "0",
			# 'X-Anit-Forge-Token': "None",
		},
		'DOWNLOAD_DELAY': 0.5,
	}

	def start_requests(self):
		while True:
			lg_comp_id = get_id('comp')
			print(lg_comp_id)
			if not lg_comp_id:
				continue
			self.item = LagouItem()
			self.item['lg_comp_id'] = lg_comp_id
			self.url = self.start_url.format(lg_comp_id=lg_comp_id)
			yield scrapy.Request(self.url, meta={'item': self.item, 'dont_redirect': True}, dont_filter=True)

	def parse(self, response):
		if '公司基本信息' not in response.text:
			return
		item = response.meta.get('item', '')
		if not item:
			return
		intro = response.xpath('.//*[@id="company_intro"]//span[@class="company_content"]//text()').extract()
		if intro:
			lg_comp_intro = ''.join(intro)
		else:
			lg_comp_intro = ''
		size = response.xpath('.//*[@id="basic_container"]/div[2]/ul/li[3]/span//text()').extract_first()
		url = response.xpath('//a[@class="hovertips"]/@href').extract_first()
		tags = response.xpath('.//*[@id="tags_container"]/div[2]/div/ul/li/text()').extract()
		if tags:
			comp_tags = [tag.strip() for tag in tags]
		else:
			comp_tags = ''
		item['lg_comp_intro'] = lg_comp_intro
		item['team_size'] = size
		item['comp_url'] = url
		item['comp_tags'] = str(comp_tags)
		return item
