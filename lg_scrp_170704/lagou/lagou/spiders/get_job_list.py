# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from lg_scrp_170704.lagou.lagou.items import LagouItem
import re
import json
import pymysql.cursors
import pymysql


class GetAllSpider(Spider):
	name = 'get_job_list'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/gongsi/j{lg_comp_id}.html'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			# "Referer": "https://www.lagou.com/jobs/list_%E7%99%BE%E5%BA%A6?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords&suginput=",
			'Accept-Encoding': "gzip, deflate, br",
			'Upgrade-Insecure-Requests': "1",
		},
		'DOWNLOAD_DELAY': 1
	}
	"""
	user_trace_token=20170612170648-026cfbd0f39d4330b02cf404bac6d999; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6
=1498480701,1498706048,1499060843,1499153853; LGUID=20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644
; _ga=GA1.2.109776163.1497258409; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAABEEAAJA7A5B9089163E244FDE311078D9478A71
; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499243280; LGRID=20170705162800-db01522e-615b-11e7-9b4e-525400f775ce
; _gid=GA1.2.1298607794.1499153855; TG-TRACK-CODE=hpage_code; SEARCH_ID=39aabb581df6400b9c84960635747ac4
; fromsite="localhost:63342"; utm_source=""; LGSID=20170705153115-eda825d1-6153-11e7-a2ec-5254005c3644
; X_HTTP_TOKEN=e4dcfb507ab9891e47a5a859901b9584
	"""
	#
	# cookies = {
	# 	'user_trace_token': '20170612170648-026cfbd0f39d4330b02cf404bac6d999',
	# 	'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1497258409,1497577951',
	# 	'LGUID': '20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644',
	# 	'_ga': 'GA1.2.109776163.1497258409',
	# 	'index_location_city': '%E5%85%A8%E5%9B%BD',
	# 	'_gid': 'GA1.2.722219593.1497427964',
	# 	'SEARCH_ID': '54c912c247bf4bdcb4c0591162734d03',
	# 	'JSESSIONID': 'ABAAABAABEEAAJA1B1DFAE62C3164498D1AAA9F6FDFA840',
	# 	'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1497580523',
	# 	'LGSID': '20170616095236-78f0c585-5236-11e7-9c6d-5254005c3644',
	# 	'LGRID': '20170616103529-7673d6b8-523c-11e7-9c6d-5254005c3644',
	# 	'TG-TRACK-CODE': 'index_search',
	# 	'_gat': '1',
	# }

	def __init__(self):
		self.connection = pymysql.connect(host='localhost', user='root', password='3646287', db='spiders',
		                                  charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()

	def start_requests(self):
		sql = "select lg_comp_id from lg_id"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for result in results:
			lg_comp_id = result['lg_comp_id']
			item = LagouItem()
			item['lg_comp_id'] = lg_comp_id
			headers = {
				"Referer": "https://www.lagou.com/gongsi/{lg_comp_id}.html".format(lg_comp_id=lg_comp_id),
			}
			url = self.start_url.format(lg_comp_id=lg_comp_id)
			yield scrapy.Request(url, meta={'item': item}, headers=headers)

	def parse(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
	# 	"""window.X_Anti_Forge_Token = '946dcfc6-bb5f-4d39-9e1b-2fa45949537e';
     #        window.X_Anti_Forge_Code = '84230520';"""
	#
	# 	token = re.search(r"window\.X_Anti_Forge_Token = '([\w-]+?)';", response.text)
	# 	code = re.search(r"window\.X_Anti_Forge_Code = '(\d+?)';", response.text)
	# 	if not token or not code:
	# 		print('no token')
	# 		return
	# 	req_headers = response.request.headers
	# 	dict = {}
	# 	dict.update(req_headers.__dict__)
	# 	headers = dict.update(
	# 		{
	# 			'X-Anit-Forge-Code': code.group(),
	# 			'X-Anit-Forge-Token': token.group(),
	# 		}
	# 	)
		headers = {
			"Referer": "https://www.lagou.com/gongsi/{lg_comp_id}.html".format(lg_comp_id=item['lg_comp_id']),
		}
		url = response.request.url
		yield scrapy.Request(url, meta={'item': item}, headers=headers, callback=self.parse_item, dont_filter=True)

	def parse_item(self, response):
		job_links = response.xpath('//a[contains(@class, "position_link")]/@href').extract()
		if not job_links:
			return
		item = response.meta.get('item', '')
		if not item:
			return
		job_ids = [re.search(r'\d+', job_link).group() for job_link in job_links]
		job_titles = response.xpath('//a[contains(@class, "position_link")]/text()').extract()
		job = dict(zip(job_ids, job_titles))
		item['job'] = json.dumps(job)
		return item



