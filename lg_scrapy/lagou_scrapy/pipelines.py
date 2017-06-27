# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LagouScrapyPipeline(object):
	def process_item(self, item, spider):
		return item


class MysqlPipeline(object):
	# 采用同步的机制写入mysql
	def __init__(self):
		# self.conn = pymysql.connect('192.168.0.106', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
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

	def process_item(self, item, spider):
		# print(type(item['id']))
		insert_sql = """
            replace into tyc_jichu_bj_intro(id, quan_cheng, companyShortName, companyFullName, city, detail_url, intro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
		self.cursor.execute(insert_sql, (item["id"], item["quan_cheng"], item["companyShortName"], item["companyFullName"], item["city"], item["detail_url"], item["intro"]))
		self.conn.commit()
		return item
