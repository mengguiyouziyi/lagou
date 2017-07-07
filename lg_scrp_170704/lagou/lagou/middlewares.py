# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy import signals
import base64
from random import choice
# from scrapy.exceptions import NotConfigured

# 代理服务器
proxyServer = "http://proxy.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H4XGPM790E93518D"
proxyPass = "2835A47D56143D62"

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ProxyMiddleware(object):
	def process_request(self, request, spider):
		request.meta["proxy"] = proxyServer
		request.headers["Proxy-Authorization"] = proxyAuth


class RedirctMiddleware(object):
	def process_response(self, request, response, spider):
		if response.status == 302 or response.status == 429:
			print('wrong status: %s, retrying~~' % response.status, request.url)
			return request.replace(url=request.url)
		elif "您操作太频繁,请稍后再访问" in response.text:
			print('您操作太频繁,请稍后再访问, retrying~~')
			return request.replace(url=request.url)
		else:
			return response


class RotateUserAgentMiddleware(object):
	"""Middleware used for rotating user-agent for each request"""

	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.get('USER_AGENT_CHOICES', []))

	def process_request(self, request, spider):
		request.headers.setdefault('User-Agent', choice(self.agents))


# class Tyc20170703SpiderMiddleware(object):
# 	# Not all methods need to be defined. If a method is not defined,
# 	# scrapy acts as if the spider middleware does not modify the
# 	# passed objects.
#
# 	@classmethod
# 	def from_crawler(cls, crawler):
# 		# This method is used by Scrapy to create your spiders.
# 		s = cls()
# 		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
# 		return s
#
# 	def process_spider_input(self, response, spider):
# 		# Called for each response that goes through the spider
# 		# middleware and into the spider.
#
# 		# Should return None or raise an exception.
# 		return None
#
# 	def process_spider_output(self, response, result, spider):
# 		# Called with the results returned from the Spider, after
# 		# it has processed the response.
#
# 		# Must return an iterable of Request, dict or Item objects.
# 		for i in result:
# 			yield i
#
# 	def process_spider_exception(self, response, exception, spider):
# 		# Called when a spider or process_spider_input() method
# 		# (from other spider middleware) raises an exception.
#
# 		# Should return either None or an iterable of Response, dict
# 		# or Item objects.
# 		pass
#
# 	def process_start_requests(self, start_requests, spider):
# 		# Called with the start requests of the spider, and works
# 		# similarly to the process_spider_output() method, except
# 		# that it doesn’t have a response associated.
#
# 		# Must return only requests (not items).
# 		for r in start_requests:
# 			yield r
#
# 	def spider_opened(self, spider):
# 		spider.logger.info('Spider opened: %s' % spider.name)