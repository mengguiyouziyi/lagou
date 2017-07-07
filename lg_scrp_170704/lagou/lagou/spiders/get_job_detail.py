# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from lagou.items import LagouItem
import json
import re
import pymysql.cursors
import pymysql


class GetAllSpider(Spider):
	name = 'get_job_detail'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/jobs/{job_id}.html'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			'Accept-Encoding': "gzip, deflate, br",
			'Upgrade-Insecure-Requests': "1",
		},
		'DOWNLOAD_DELAY': 1
	}

	def __init__(self):
		self.connection = pymysql.connect(host='localhost', user='root', password='3646287', db='spiders',
		                                  charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()

	def start_requests(self):
		sql = "select lg_comp_id, job from lg_id"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for result in results:
			lg_comp_id = result['lg_comp_id']
			job = result['job']
			item = LagouItem()
			item['lg_comp_id'] = lg_comp_id
			item['job'] = job
			job = dict(json.loads(job))
			job_id = job.keys()[0]
			job_link = self.start_url.format(job_id=job_id)
			yield scrapy.Request(job_link, meta={'item': item})

	def parse(self, response):
		comp_url = response.xpath('.//*[@id="job_company"]/dd/ul/li[4]/a/@href').extract_first()
		if not comp_url:
			return
		item = response.meta.get('item', '')
		if not item:
			return
		item['comp_url'] = comp_url
		return item




