# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
	# define the fields for your item here like:
	# get from redis
	lg_comp_id = scrapy.Field()
	# get from company page
	lg_short_name = scrapy.Field()
	comp_url = scrapy.Field()
	lg_comp_name = scrapy.Field()
	lg_comp_intro = scrapy.Field()
	team_size = scrapy.Field()
	comp_tags = scrapy.Field()
	# get from job_list page
	job = scrapy.Field()


