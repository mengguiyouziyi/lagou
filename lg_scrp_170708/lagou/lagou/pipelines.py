# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# from scrapy.exceptions import DropItem
# from .utils.bloomfilter import PyBloomFilter, conn


class MysqlPipeline(object):
	"""
	本机localhost；公司etl2.innotree.org；服务器etl1.innotree.org
	"""
	def __init__(self):
		self.conn = pymysql.connect(host='etl1.innotree.org', user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		sql = """insert into lg_all(lg_comp_id, lg_short_name, comp_url, lg_comp_name, lg_comp_intro, team_size, comp_tags, job) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE lg_short_name=VALUES(lg_short_name), comp_url=VALUES(comp_url), lg_comp_name=VALUES(lg_comp_name), lg_comp_intro=VALUES(lg_comp_intro), team_size=VALUES(team_size), comp_tags=VALUES(comp_tags), job=VALUES(job)"""
		args = (item["lg_comp_id"], item["lg_short_name"], item["comp_url"], item['lg_comp_name'], item['lg_comp_intro'], item["team_size"], item['comp_tags'], item['job'])
		self.cursor.execute(sql, args=args)
		self.conn.commit()
		print(str(item['lg_comp_id']) + ' success')


# class DuplicatesPipeline(object):
# 	def __init__(self):
# 		self.bf = PyBloomFilter(conn=conn, key='item_filter')
#
# 	def process_item(self, item, spider):
# 		if self.bf.is_exist(str(item['lg_comp_id'])):
# 			raise DropItem("Duplicate item found: ")
# 		else:
# 			self.bf.add(str(item['lg_comp_id']))
# 			return item
