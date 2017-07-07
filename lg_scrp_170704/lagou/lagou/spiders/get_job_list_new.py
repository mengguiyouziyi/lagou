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
	name = 'get_job_list_new'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/gongsi/searchPosition.json'
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
			# "Referer": "https://www.lagou.com/jobs/list_%E7%99%BE%E5%BA%A6?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords&suginput=",
			'Accept-Encoding': "gzip, deflate, br",
			'X-Requested-With': "X-Requested-With",
		},
		# 'CONCURRENT_REQUESTS': 32,
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
		self.headerss = []
		self.form_datas = []
		for result in results:
			lg_comp_id = result['lg_comp_id']
			item = LagouItem()
			item['lg_comp_id'] = lg_comp_id
			headers = {
				"Referer": "https://www.lagou.com/gongsi/j{lg_comp_id}.html".format(lg_comp_id=lg_comp_id),
			}
			form_data = {
				'companyId': str(lg_comp_id),
				'pageNo': '1',
				'pageSize': '10',
				'positionFirstType': '全部',
			}
			self.items.append(item)
			self.headerss.append(headers)
			self.form_datas.append(form_data)

	def start_requests(self):
		for form_data, item, headers in zip(self.form_datas, self.items, self.headerss):
			yield scrapy.FormRequest(self.start_url, formdata=form_data, meta={'item': item, 'form_data': form_data},
			                         headers=headers,
			                         dont_filter=True)

	def parse(self, response):
		# 	item = response.meta.get('item', '')
		# 	if not item:
		# 		return
		# 	headers = {
		# 		"Referer": "https://www.lagou.com/gongsi/j{lg_comp_id}.html".format(lg_comp_id=item['lg_comp_id']),
		# 	}
		# 	url = response.request.url
		# 	form_data = {
		# 		'companyId': int(item['lg_comp_id']),
		# 		'pageNo': 1,
		# 		'pageSize': 10,
		# 		'positionFirstType': '全部',
		# 	}
		# 	yield scrapy.FormRequest(url, formdata=form_data, meta={'item': item}, headers=headers, callback=self.parse_item)
		#
		# def parse_item(self, response):
		print('meta~~~~' + str(response.meta['form_data']))
		item = response.meta.get('item', '')
		if not item:
			return
		api = json.loads(response.text)
		if 'content' not in api.keys():
			return
		if 'data' not in api['content'].keys():
			return
		if 'page' not in api['content']['data'].keys():
			return
		page = api['content']['data']['page']
		page_no = page['pageNo']
		next_page = int(page_no) + 1
		totalCount = page['totalCount']
		results = api['content']['data']['page']['result']
		if not results:
			return

		job_ids = [result['positionId'] for result in results]
		job_titles = [result['positionName'] for result in results]

		job_id = response.meta.get('job_ids', [])
		job_title = response.meta.get('job_titles', [])
		job_ids.extend(job_id)
		job_titles.extend(job_title)

		if next_page <= int(totalCount) / 10:

			form_data = response.meta['form_data']
			form_data.update({
				'pageNo': str(next_page),
			})
			yield scrapy.FormRequest(self.start_url, formdata=form_data,
			                         meta={'item': item, 'form_data': form_data, 'job_ids': job_ids,
			                               'job_titles': job_titles},
			                         headers=response.request.headers, callback=self.parse,
			                         dont_filter=True)
			print('next---' + str(response.meta['form_data']))
		else:
			job = dict(zip(job_ids, job_titles))
			item['job'] = json.dumps(job, ensure_ascii=False)
			yield item
