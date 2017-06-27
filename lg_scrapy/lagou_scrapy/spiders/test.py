# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
import json
import pymysql
from lagou_scrapy.items import DescItem
from urllib.parse import quote


class LagouSpider(Spider):
	name = 'lagou2'

	def __init__(self):
		self.conn = pymysql.connect(
			# host='10.44.60.141',
			host='101.200.166.12',
			user='spider',
			password='spider',
			db='spider',
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor,
			use_unicode=True
		)
		self.cursor = self.conn.cursor()
		self.cookies = {
			'user_trace_token': '20170612170648-026cfbd0f39d4330b02cf404bac6d999',
			'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1497258409,1497577951',
			'LGUID': '20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644',
			'_ga': 'GA1.2.109776163.1497258409',
			'index_location_city': '%E5%85%A8%E5%9B%BD',
			'_gid': 'GA1.2.722219593.1497427964',
			'SEARCH_ID': '54c912c247bf4bdcb4c0591162734d03',
			'JSESSIONID': 'ABAAABAABEEAAJA1B1DFAE62C3164498D1AAA9F6FDFA840',
			'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1497580523',
			'LGSID': '20170616095236-78f0c585-5236-11e7-9c6d-5254005c3644',
			'LGRID': '20170616103529-7673d6b8-523c-11e7-9c6d-5254005c3644',
			'TG-TRACK-CODE': 'index_search',
			'_gat': '1',
		}

	def start_requests(self):
		item = DescItem()

		get_sql = """select id,quan_cheng from tyc_jichu_bj where id < 1000"""
		try:
			self.cursor.execute(get_sql)
		except Exception as e:
			print("Error%s: unable to fecth data" % str(e))
			pass
		else:
			many = self.cursor.fetchall()
			for row in many:
				id = row['id']
				quan_cheng = row['quan_cheng']
				item['id'] = id
				item['quan_cheng'] = quan_cheng

				url = 'https://www.lagou.com/jobs/companyAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=true&first=true&kd={}&pn=1'.format(quote(quan_cheng))

				yield scrapy.Request(url, meta={'item': item}, cookies=self.cookies)
				pass
		finally:
			self.conn.close()

	def parse(self, response):
		item = response.meta['item']

		dum = dict(json.loads(response.text))
		result = dum.get('content', {}).get('result', {})
		print(str(item['quan_cheng']) + ':' + str(result))
		# 搜索结果为空
		if not result:
			print('no intro:' + str(item['id']) + ':' + item['quan_cheng'])
			pass
		else:
			companyId = result[0].get("companyId", 0)
			city = result[0].get("city", "")
			companyShortName = result[0].get("companyShortName", "")
			companyFullName = result[0].get("companyFullName", "")

			detail_url = 'https://www.lagou.com/gongsi/%d.html' % companyId
			item['companyShortName'] = companyShortName
			item['companyFullName'] = companyFullName
			item['city'] = city
			item['detail_url'] = detail_url

			yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item}, cookies=self.cookies)

	def parse_detail(self, response):
		item = response.meta['item']
		desc_list = response.xpath('//span[@class="company_content"]//text()').extract()
		print(desc_list)
		# 如果有公司介绍
		if desc_list:
			print('have:' + str(item['id']) + '~~' + item['quan_cheng'] + '~~' + response.url)
			intro = ''.join([desc for desc in desc_list])
			item['intro'] = intro
			return item
