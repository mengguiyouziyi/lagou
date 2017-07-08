# coding:utf-8

from my_redis import QueueRedis
import pymysql
import time
from bloomfilter import PyBloomFilter, conn
import redis

import os
import sys
from os.path import dirname

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def handle(type):
	"""
	过滤并添加队列，需阻塞运行
	"""
	# 本机2，服务器和家1
	connection = pymysql.connect(host='etl1.innotree.org', user='spider', password='spider', db='spider', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	sql = "select lg_comp_id from lg_id"
	cursor.execute(sql)
	results = cursor.fetchall()
	if type == 'comp':
		key = 'comp_filter'
	else:
		key = 'job_filter'
	bf = PyBloomFilter(conn=conn, key=key)
	red = QueueRedis()

	for result in results:
		lg_comp_id = result['lg_comp_id']
		if bf.is_exist(str(lg_comp_id)):
			print('is_exist %d' % lg_comp_id)
			continue
		else:
			print('not exist %d' % lg_comp_id)
			bf.add(str(lg_comp_id))
			if type == 'comp':
				red.send_to_queue('comp_que', lg_comp_id)
			else:
				red.send_to_queue('job_que', lg_comp_id)


def main(type):
	while True:
		handle(type)
		time.sleep(3600)

def get_id(type):
	red = QueueRedis()
	que_key = 'comp_que' if type == 'comp' else 'job_que'
	results = red.read_from_queue(que_key, 1)
	if results:
		result = int(results[0])
		return result
	else:
		return 0

if __name__ == '__main__':
	# main('comp')
	main('job')
