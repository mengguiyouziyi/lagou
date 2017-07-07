# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
from .utils.bloomfilter import PyBloomFilter, conn
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


class LagouItem(object):
	def process_item(self, item, spider):
		return item


class MysqlPipeline(object):
	# 采用同步的机制写入mysql
	def __init__(self):
		self.conn = pymysql.connect(host='etl1.innotree.org', user='spider', password='spider', db='spider',
		                                  charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if spider.name == 'get_all_search':
			sql = """replace into lg_id(id, quan_cheng, lg_comp_id, lg_comp_name) VALUES (%s, %s, %s, %s)"""
			args = (item["id"], item["quan_cheng"], item["lg_comp_id"], item["lg_comp_name"])
		elif spider.name == 'get_comp':
			# sql = "insert into lg_id(lg_comp_intro, team_size, comp_tags) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE lg_comp_id=VALUES(%s)"
			sql = """update lg_id set lg_comp_intro=%s, team_size=%s, comp_url=%s, comp_tags=%s WHERE lg_comp_id=%s"""
			args = (item["lg_comp_intro"], item["team_size"], item["comp_url"], item['comp_tags'], item['lg_comp_id'])
		elif spider.name == 'get_job_list_new':
			# sel_sql = """select job from lg_id WHERE lg_comp_id=%s"""
			# self.cursor.execute(sel_sql, (item['lg_comp_id'],))
			# result = self.cursor.fetchone()
			# if result['job'] != 'null' and item['job'] and result['job']:
			# 	print('表中有，取出来的' + str(result['job']) + str(item['job']))
			# 	job = json.dumps(json.loads(result['job']).update(json.loads(item['job'])))
			# else:
			# 	job = item['job']
			# 	print('表中没有，返回网站取的item' + str(job))

			sql = """update lg_id set job=%s WHERE lg_comp_id=%s"""
			args = (item['job'], item['lg_comp_id'])
		# elif spider.name == 'get_job_detail':
		# 	sql = """update lg_id set comp_url=%s WHERE lg_comp_id=%s"""
		# 	args = (item["comp_url"], item['lg_comp_id'])
		self.cursor.execute(sql, args=args)
		print('success')

		self.conn.commit()


class DuplicatesPipeline(object):
	def __init__(self):
		# if spider.name == 'get_all_search':
		# 	key = 'se_fil'
		# elif spider.name == 'get_comp':
		# 	key = 'comp_fil'
		# elif spider.name == 'get_job_list':
		# 	key = 'job_list_fil'
		# elif spider.name == 'get_job_detail':
		# 	key = 'job_de_fil'
		self.bf = PyBloomFilter(conn=conn, key='lg_comp_id')

	def process_item(self, item, spider):
		if self.bf.is_exist(str(item['lg_comp_id'])):
			raise DropItem("Duplicate item found: ")
		else:
			self.bf.add(str(item['lg_comp_id']))
			return item
