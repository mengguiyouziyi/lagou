# coding:utf-8

import os
import sys
from os.path import dirname

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)

import redis
from my_redis import QueueRedis

"""
本机localhost；服务器a027.hb2.innotree.org
"""
pool = redis.ConnectionPool(host='a027.hb2.innotree.org', port=6379, db=0)
conn = redis.StrictRedis(connection_pool=pool)
red = QueueRedis()


def send_id():
	for id in range(230001):
		red.send_to_queue('ids', id)


if __name__ == '__main__':
	send_id()