# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
	# define the fields for your item here like:
	# get from db
	id = scrapy.Field()
	quan_cheng = scrapy.Field()
	# get from api
	lg_comp_id = scrapy.Field()
	lg_comp_name = scrapy.Field()
	# get from company page
	lg_comp_intro = scrapy.Field()
	team_size = scrapy.Field()
	comp_tags = scrapy.Field()
	comp_url = scrapy.Field()
	# get from job_list page
	job = scrapy.Field()


