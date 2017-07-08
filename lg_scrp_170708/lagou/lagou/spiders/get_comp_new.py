# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
import json
from lagou.items import LagouItem
from lagou.utils.get import get_id


class GetAllSpider(Spider):
	name = 'get_comp'
	allowed_domains = ['lagou.com']
	com_url = 'https://www.lagou.com/gongsi/{lg_comp_id}.html'
	job_url = 'https://www.lagou.com/gongsi/searchPosition.json'
	custom_settings = {
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
			lg_comp_id = get_id()
		# 	lg_comp_id = 225916
			print(lg_comp_id)
			if not lg_comp_id:
				continue
			self.item = LagouItem()
			self.item['lg_comp_id'] = lg_comp_id
			self.url = self.com_url.format(lg_comp_id=lg_comp_id)
			yield scrapy.Request(self.url, meta={'item': self.item, 'dont_redirect': True}, dont_filter=True)

	def parse(self, response):
		if 'page404' in response.text:
			return
		item = response.meta.get('item', '')
		if not item:
			return
		lg_comp_id = item['lg_comp_id']
		hovertips = response.xpath('//a[@class="hovertips"]')
		short = hovertips.xpath('./text()').extract_first().strip()
		long = hovertips.xpath('./@title').extract_first().strip()
		url_unknown = hovertips.xpath('./@href').extract_first()
		url = url_unknown if url_unknown else ''
		if 'lagou.com/gongsi/' in url:
			url = ''

		intro = response.xpath('.//*[@id="company_intro"]//span[@class="company_content"]//text()').extract()
		lg_comp_intro = ''.join(intro)
		size_un = response.xpath('.//*[@id="basic_container"]/div[2]/ul/li[3]/span//text()').extract_first()
		size = size_un if size_un else ''
		tags = response.xpath('.//*[@id="tags_container"]/div[2]/div/ul/li/text()').extract()
		if tags:
			comp_tags = [tag.strip() for tag in tags]
		else:
			comp_tags = ''
		item['lg_short_name'] = short
		item['lg_comp_name'] = long
		item['comp_url'] = url
		item['lg_comp_intro'] = lg_comp_intro
		item['team_size'] = size
		item['comp_tags'] = str(comp_tags)
		job_num = response.xpath('//div[@class="company_data"]/ul/li[1]/strong/text()').extract_first()
		"""
		有else和没有else区别是：
		如果没有职位，直接返回item；
		如果有职位，则进行后续获取job的操作
		"""
		if '暂无' in job_num:
			item['job'] = ''
			yield item
		else:
			self.headers = {
				"Referer": "https://www.lagou.com/gongsi/j{lg_comp_id}.html".format(lg_comp_id=lg_comp_id),
			}
			self.form_data = {
				'companyId': str(lg_comp_id),
				'pageNo': '1',
				'pageSize': '10',
				'positionFirstType': '全部',
			}
			yield scrapy.FormRequest(self.job_url, formdata=self.form_data,
			                         meta={'item': item, 'form_data': self.form_data},
			                         headers=self.headers, dont_filter=True, callback=self.parse_job)


	def parse_job(self, response):
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

		totalCount = page['totalCount']
		results = api['content']['data']['page']['result']
		if not results:
			return

		job_ids = [result['positionId'] for result in results]
		job_titles = [result['positionName'] for result in results]
		# 不管有没有下一页，都会进行此步操作
		job_id = response.meta.get('job_ids', [])
		job_title = response.meta.get('job_titles', [])
		job_ids.extend(job_id)
		job_titles.extend(job_title)

		next_page = int(page_no) + 1
		if next_page <= int(totalCount) / 10:
			form_data = response.meta['form_data']
			form_data.update({
				'pageNo': str(next_page),
			})
			yield scrapy.FormRequest(self.job_url, formdata=form_data,
			                         meta={'item': item, 'form_data': form_data, 'job_ids': job_ids,
			                               'job_titles': job_titles},
			                         headers=response.request.headers, callback=self.parse_job,
			                         dont_filter=True)
			# print('next---' + str(response.meta['form_data']))
		else:
			job = dict(zip(job_ids, job_titles))
			item['job'] = json.dumps(job, ensure_ascii=False)
			yield item


