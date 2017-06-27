# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DescItem(scrapy.Item):
	id = scrapy.Field()
	quan_cheng = scrapy.Field()
	companyShortName = scrapy.Field()
	companyFullName = scrapy.Field()
	city = scrapy.Field()
	intro = scrapy.Field()
	detail_url = scrapy.Field()


# class CompanyItem(scrapy.Item):
# 	#header
# 	company_id = scrapy.Field() #企业id
# 	company_url = scrapy.Field() #企业url
# 	url_object_id = scrapy.Field() #url hash
# 	company_name = scrapy.Field() #企业名
# 	identify = scrapy.Field() #企业认证类别
# 	company_word = scrapy.Field() #企业短语
# 	job_num = scrapy.Field() #招聘岗位数量
# 	finish_rate = scrapy.Field() #该公司所有职位收到的简历中，在投递后7天内处理完成的简历所占比例
# 	finish_time = scrapy.Field() #该公司的所有职位管理者完成简历处理的平均用时
# 	interview_appraisal = scrapy.Field() #该公司收到的面试评价数量
# 	last_leave_time = scrapy.Field() #该公司职位管理者最近一次登录时间
# 	#产品信息
# 	product_list = scrapy.Field() #产品名称列表
# 	#公司简介
# 	company_des = scrapy.Field() #公司简介
# 	company_pic_url_list = scrapy.Field()
# 	#发展历程
# 	company_history_list = scrapy.Field()
# 	#面试评价
# 	interview_star = scrapy.Field() #综合评分
# 	accord_star = scrapy.Field() #描述相符度评分
# 	interviewer_star = scrapy.Field() #面试官评分
# 	environment_star = scrapy.Field() #公司环境评分
# 	#地图
# 	company_location_list = scrapy.Field()
# 	#公司基本信息
# 	company_type = scrapy.Field() #移动互联网
# 	company_process = scrapy.Field() #上市公司
# 	employee_num = scrapy.Field()
# 	company_location = scrapy.Field()
# 	#公司领导
#
#
#
#
# 	crawl_time = scrapy.Field()
#
#
# class ProductItem(scrapy.Item):
# 	pass
#
#
# class CompanyPicItem(scrapy.Item):
# 	pass
#
#
# class HistoryItem(scrapy.Item):
# 	pass
#
#
# class InterviewItem(scrapy.Item):
# 	pass
#
#
# class LocationItem(scrapy.Item):
# 	pass
#
#
# class JobItem(scrapy.Item):
# 	pass