# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from lagou.items import LagouItem
import json
from lagou.utils.mysql2redis import get_id


class GetAllSpider(Spider):
	name = 'get_job_list_new2'
	allowed_domains = ['lagou.com']
	start_url = 'https://www.lagou.com/gongsi/searchPosition.json'
	custom_settings = {
		'DOWNLOADER_MIDDLEWARES': {
			'lagou.middlewares.ProxyMiddleware': 1,
			'lagou.middlewares.RedirctMiddleware': 110,
			'lagou.middlewares.RotateUserAgentMiddleware': 2,
		},
		'DEFAULT_REQUEST_HEADERS': {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			'Accept-Encoding': "gzip, deflate, br",
			'X-Requested-With': "X-Requested-With",
		},
		'DOWNLOAD_DELAY': 0.5,
	}

	def start_requests(self):
		while True:
			lg_comp_id = get_id('job')
			print(lg_comp_id)
			if not lg_comp_id:
				continue
			self.item = LagouItem()
			self.item['lg_comp_id'] = lg_comp_id
			self.headers = {
				"Referer": "https://www.lagou.com/gongsi/j{lg_comp_id}.html".format(lg_comp_id=lg_comp_id),
			}
			self.form_data = {
				'companyId': str(lg_comp_id),
				'pageNo': '1',
				'pageSize': '10',
				'positionFirstType': '全部',
			}
			yield scrapy.FormRequest(self.start_url, formdata=self.form_data,
			                         meta={'item': self.item, 'form_data': self.form_data},
			                         headers=self.headers, dont_filter=True)

	def parse(self, response):
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
