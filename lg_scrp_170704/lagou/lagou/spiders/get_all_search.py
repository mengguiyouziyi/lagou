# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from lagou.items import LagouItem
import json
import pymysql.cursors
import pymysql
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


class GetAllSpider(Spider):
	name = 'get_all_search'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/jobs/companyAjax.json'
	custom_settings = {

		'DOWNLOADER_MIDDLEWARES': {
			'lagou.middlewares.ProxyMiddleware': 1,
			'lagou.middlewares.RedirctMiddleware': 110,
			'lagou.middlewares.RotateUserAgentMiddleware': 2,
		},
		'ITEM_PIPELINES': {
			'lagou.pipelines.MysqlPipeline': 300,
			'lagou.pipelines.DuplicatesPipeline': 1,
		},
		'DEFAULT_REQUEST_HEADERS': {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			"Referer": "https://www.lagou.com/jobs/list_%E7%99%BE%E5%BA%A6?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=",
			# 'X-Anit-Forge-Code': "0",
			# 'X-Anit-Forge-Token': "None",
			'X-Requested-With': "XMLHttpRequest",
			'Accept-Encoding': "gzip, deflate, br",
		},
		# 'CONCURRENT_REQUESTS': 100,
		'DOWNLOAD_DELAY': 0.5,
		# 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
		# 'CONCURRENT_REQUESTS_PER_IP': 16,
		# 'AUTOTHROTTLE_ENABLED': True,
		# 'AUTOTHROTTLE_START_DELAY': 5.0,
		# 'AUTOTHROTTLE_MAX_DELAY': 60.0,
		# 'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.5,
		# 'AUTOTHROTTLE_DEBUG': True,
	}
	"""
	1-1、limit 130000
	1-2、limit 130000,120000
	2-1、limit 250000,130000
	2-2、limit 380000,120000
	3-1、limit 500000,130000
	3-2、limit 630000,120000
	4-1、limit 750000,130000
	4-2、limit 880000,120000
	5-1、limit 1000000,130000
	5-2、limit 1130000,120000
	6-1、limit 1250000,130000
	6-2、limit 1380000,250000
	"""
	def __init__(self):
		self.connection = pymysql.connect(host='etl1.innotree.org', user='spider', password='spider', db='spider',
		                                  charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()
		sql = "select id, quan_cheng from tyc_jichu_bj ORDER BY id limit 630000,120000"
		# sql = "select id, quan_cheng from tyc_jichu_bj ORDER BY id limit 250"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		self.form_datas = []
		self.items = []
		for result in results:
			id = result['id']
			quan_cheng = result['quan_cheng']
			item = LagouItem()
			item['id'] = id
			item['quan_cheng'] = quan_cheng
			if len(quan_cheng) > 10:
				key = quan_cheng[3:10]
			else:
				key = quan_cheng
			form_data = {'first': 'true', 'kd': key, 'pn': '1'}
			self.form_datas.append(form_data)
			self.items.append(item)

	def start_requests(self):
		for form_data, item in zip(self.form_datas, self.items):
			yield scrapy.FormRequest(self.start_url, formdata=form_data, meta={'item': item, 'form_data': form_data},
			                         dont_filter=True)

	def parse(self, response):
		# print('meta' + str(response.meta['form_data']))
		api = json.loads(response.text)
		if not api['success']:
			return
		item = response.meta.get('item', '')
		if not item:
			return
		content = api['content']
		results = content['result']
		for result in results:
			item['lg_comp_id'] = result['companyId']
			item['lg_comp_name'] = result['companyFullName']
			yield item

		hasNextPage = content['hasNextPage']
		if not hasNextPage:
			return

		currentPageNo = content['currentPageNo']
		nextPageNo = int(currentPageNo) + 1
		form_data = response.meta['form_data']
		form_data.update({'pn': str(nextPageNo)})
		yield scrapy.FormRequest(self.start_url, meta={'item': item, 'form_data': form_data}, formdata=form_data,
		                         callback=self.parse, dont_filter=True)
		# print('next' + str(item) + str(form_data))
