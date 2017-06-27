# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
import json
import pymysql
from lagou_scrapy.items import DescItem


class LagouSpider(Spider):
	name = 'lagou'

	def __init__(self):
		# self.conn = pymysql.connect(host='101.200.166.12', user='spider', password='spider', db='spider', charset="utf8mb4")
		self.conn = pymysql.connect(
			host='101.200.166.12',
			user='spider',
			password='spider',
			db='spider',
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor,
			use_unicode=True
		)
		self.cursor = self.conn.cursor()

	def start_requests(self):
		item = DescItem()
		get_sql = """select id, quan_cheng from tyc_jichu_bj"""
		try:
			self.cursor.execute(get_sql)
		except Exception as e:
			print("Error%s: unable to fecth data" % str(e))
			pass
		else:
			many = self.cursor.fetchmany(size=5)
			for row in many:
				id = row[0]
				quan_cheng = row[1]
				item['id'] = id
				item['quan_cheng'] = quan_cheng

				print('id=%d, quan_cheng%s' % (id, quan_cheng))
				url = 'https://www.lagou.com/jobs/companyAjax.json'
				# meta = {'first': 'true', 'kd': '上海德威企业发展股份有限公司', 'pn': '1'}
				form_data = {'first': 'true', 'kd': '%s' % quan_cheng, 'pn': '1'}

				return [scrapy.FormRequest(url, formdata=form_data, meta={'item': item})]
		finally:
			self.conn.close()

	def parse(self, response):
		item = response.meta['item']

		dum = dict(json.loads(response.text))
		result = dum.get('content', {}).get('result', {})
		# 搜索结果为空
		if not result: pass
		# interviewRemarkNum = result[0].get("interviewRemarkNum", 0)
		# processRate = result[0].get("processRate", 0)
		# countryScore = result[0].get("countryScore", 0)
		# cityScore = result[0].get("cityScore", 0)
		companyId = result[0].get("companyId", 0)
		# industryField = result[0].get("industryField", "")
		city = result[0].get("city", "")
		# createTime = result[0].get("createTime", '')
		# companySize = result[0].get("companySize", '')
		companyShortName = result[0].get("companyShortName", "")
		# companyLogo = result[0].get("companyLogo", "")
		# financeStage = result[0].get("financeStage", "")
		# approve = result[0].get("approve", 0)
		# companyFeatures = result[0].get("companyFeatures", "")
		companyFullName = result[0].get("companyFullName", "")
		# positionNum = result[0].get("positionNum", 0)

		detail_url = 'https://www.lagou.com/gongsi/%d.html' % companyId
		item['companyShortName'] = companyShortName
		item['companyFullName'] = companyFullName
		item['city'] = city
		item['detail_url'] = detail_url

		return [scrapy.Request(detail_url, callback=self.parse_detail, meta={'item':item})]

	def parse_detail(self, response):
		item = response.meta['item']
		desc_list = response.xpath('//span[@class="company_content"]//text()').extract()
		# 如果有公司介绍
		if desc_list:
			intro = desc_list[0]
			item['intro'] = intro
			return item

