# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from lagou.items import LagouItem
import pymysql.cursors
import pymysql


class GetAllSpider(Spider):
	name = 'get_comp'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/gongsi/{lg_comp_id}.html'
	custom_settings = {
		'LOG_STDOUT': False,
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
		# 'CONCURRENT_REQUESTS': 16,
		'DOWNLOAD_DELAY': 0.5,
		# 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
		# 'CONCURRENT_REQUESTS_PER_IP': 16,
		# 'AUTOTHROTTLE_ENABLED': True,
		# 'AUTOTHROTTLE_START_DELAY': 5.0,
		# 'AUTOTHROTTLE_MAX_DELAY': 60.0,
		# 'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
		# 'AUTOTHROTTLE_DEBUG': True,
	}
	"""
	共240000
	1-1、limit 20000
	1-2、limit 20000,20000
	2-1、limit 40000,20000
	2-2、limit 60000,20000
	3-1、limit 80000,20000
	3-2、limit 100000,20000
	4-1、limit 120000,20000
	4-2、limit 140000,20000
	5-1、limit 160000,20000
	5-2、limit 180000,20000
	6-1、limit 200000,20000
	6-2、limit 220000,-1
	"""
	def __init__(self):
		self.connection = pymysql.connect(host='etl1.innotree.org', user='spider', password='spider', db='spider',
		                                  charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()
		sql = "select lg_comp_id from lg_id ORDER BY lg_comp_id limit 20000"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		self.items = []
		self.urls = []
		for result in results:
			lg_comp_id = result['lg_comp_id']
			item = LagouItem()
			item['lg_comp_id'] = lg_comp_id
			url = self.start_url.format(lg_comp_id=lg_comp_id)
			self.items.append(item)
			self.urls.append(url)

	def start_requests(self):
		for url, item in zip(self.urls, self.items):
			yield scrapy.Request(url, meta={'item': item, 'dont_redirect': True}, dont_filter=True)

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
		# intro = re.search(r'\"companyProfile\"\:\"(.*)')
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
