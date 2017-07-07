# coding=utf-8
from requests.sessions import session
import requests
import pymysql
import json
from scrapy.selector import Selector
import random, time, datetime
from multiprocessing import Pool
from fake_useragent import UserAgent


class GetIntro(object):
	def __init__(self, *args, **kwargs):
		self.conn = pymysql.connect(
			host='10.44.60.141',
			# host='101.200.166.12',
			user='spider',
			password='spider',
			db='spider',
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor,
			use_unicode=True
		)
		self.cursor = self.conn.cursor()
		self.ua = UserAgent()
		# self.cookies = [
		# 	'user_trace_token=20170612170648-026cfbd0f39d4330b02cf404bac6d999; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497258409,1497577951; LGUID=20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644; _ga=GA1.2.109776163.1497258409; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.722219593.1497427964; SEARCH_ID=8ed5770ccb9d4b99b174c1d9e1b93fdd; JSESSIONID=ABAAABAABEEAAJA1B1DFAE62C3164498D1AAA9F6FDFA840; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497594024; LGRID=20170616142030-e5896203-525b-11e7-9c6d-5254005c3644; TG-TRACK-CODE=index_search; LGSID=20170616135506-5900b1fa-5258-11e7-9bc5-525400f775ce',
		# 	'user_trace_token=20170611162631-ac0e66cb-4e7f-11e7-83ee-525400f775ce; LGUID=20170611162631-ac0e6aae-4e7f-11e7-83ee-525400f775ce; fromsite="localhost:63342"; JSESSIONID=ABAAABAABEEAAJABF9E692B8A110EAC1E5B8D41DCB395EF; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _putrc=4F9D5E0356A7F682; login=true; unick=%E5%AD%99%E7%AB%8B%E5%BB%BA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; TG-TRACK-CODE=index_search; _gid=GA1.2.805528246.1497530341; _ga=GA1.2.200265071.1497169588; LGSID=20170617125231-c53b4db5-5318-11e7-9c6f-5254005c3644; LGRID=20170617125253-d279455a-5318-11e7-9cb7-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497257843,1497270178,1497439331,1497675144; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497675166; SEARCH_ID=c420f95450ed43b1aac4e94524e157aa; index_location_city=%E5%8C%97%E4%BA%AC',
		# 	'user_trace_token=20170611162631-ac0e66cb-4e7f-11e7-83ee-525400f775ce; LGUID=20170611162631-ac0e6aae-4e7f-11e7-83ee-525400f775ce; fromsite="localhost:63342"; JSESSIONID=ABAAABAABEEAAJABF9E692B8A110EAC1E5B8D41DCB395EF; _putrc=4F9D5E0356A7F682; login=true; unick=%E5%AD%99%E7%AB%8B%E5%BB%BA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; TG-TRACK-CODE=index_search; _gid=GA1.2.805528246.1497530341; _ga=GA1.2.200265071.1497169588; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497257843,1497270178,1497439331,1497675144; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497675187; LGRID=20170617125314-df4f1bb2-5318-11e7-9cb8-525400f775ce; SEARCH_ID=5220eaf2c7984c2a82cb444855c488f6; index_location_city=%E5%8C%97%E4%BA%AC',
		# 	'user_trace_token=20170612170648-026cfbd0f39d4330b02cf404bac6d999; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497258409,1497577951; LGUID=20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644; _ga=GA1.2.109776163.1497258409; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.722219593.1497427964; SEARCH_ID=3a924c638aad4c7fb4b7ae36b26d440e; JSESSIONID=ABAAABAABEEAAJA1B1DFAE62C3164498D1AAA9F6FDFA840; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497678584; LGRID=20170617134952-c834c774-5320-11e7-9c70-5254005c3644; TG-TRACK-CODE=index_search; _gat=1; LGSID=20170617134948-c5c76755-5320-11e7-9cd0-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D36.110.41.42'
		# 	'user_trace_token=20170611162631-ac0e66cb-4e7f-11e7-83ee-525400f775ce; LGUID=20170611162631-ac0e6aae-4e7f-11e7-83ee-525400f775ce; fromsite="localhost:63342"; JSESSIONID=ABAAABAABEEAAJABF9E692B8A110EAC1E5B8D41DCB395EF; _putrc=4F9D5E0356A7F682; login=true; unick=%E5%AD%99%E7%AB%8B%E5%BB%BA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; TG-TRACK-CODE=index_search; _ga=GA1.2.200265071.1497169588; _gid=GA1.2.805528246.1497530341; LGSID=20170617134823-935e1867-5320-11e7-9c70-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%2520%25E5%258C%2597%25E4%25BA%25AC%25E9%2598%25BF%25E5%25B0%2594%25E6%25B3%2595%25E6%258A%2595%25E8%25B5%2584%25E9%259B%2586%25E5%259B%25A2%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%2520%25E5%258C%2597%25E4%25BA%25AC%25E4%25B8%25AD%25E7%2594%25B5%25E5%258D%2593%25E8%2583%25BD%25E6%2595%2599%25E8%2582%25B2%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20170617134823-935e1a54-5320-11e7-9c70-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497257843,1497270178,1497439331,1497675144; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497678496; SEARCH_ID=91273cccf7db411ba100db9e6a936bc5; index_location_city=%E5%8C%97%E4%BA%AC',
		# 	'user_trace_token=20170611162631-ac0e66cb-4e7f-11e7-83ee-525400f775ce; LGUID=20170611162631-ac0e6aae-4e7f-11e7-83ee-525400f775ce; fromsite="localhost:63342"; JSESSIONID=ABAAABAABEEAAJABF9E692B8A110EAC1E5B8D41DCB395EF; _putrc=4F9D5E0356A7F682; login=true; unick=%E5%AD%99%E7%AB%8B%E5%BB%BA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; TG-TRACK-CODE=index_search; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%2520%25E5%258C%2597%25E4%25BA%25AC%25E9%2598%25BF%25E5%25B0%2594%25E6%25B3%2595%25E6%258A%2595%25E8%25B5%2584%25E9%259B%2586%25E5%259B%25A2%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%2520%25E5%258C%2597%25E4%25BA%25AC%25E4%25B8%25AD%25E7%2594%25B5%25E5%258D%2593%25E8%2583%25BD%25E6%2595%2599%25E8%2582%25B2%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; _gid=GA1.2.805528246.1497530341; _ga=GA1.2.200265071.1497169588; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497257843,1497270178,1497439331,1497675144; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497679473; LGSID=20170617134823-935e1867-5320-11e7-9c70-5254005c3644; LGRID=20170617140441-da0efd17-5322-11e7-9c70-5254005c3644; SEARCH_ID=24cd7522dd974eb997ba288cbb648b7f; index_location_city=%E5%8C%97%E4%BA%AC',
		# 	'user_trace_token=20170612170648-026cfbd0f39d4330b02cf404bac6d999; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497258409,1497577951; LGUID=20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644; _ga=GA1.2.109776163.1497258409; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.722219593.1497427964; SEARCH_ID=ef064afaad504da286fff87b92b32359; JSESSIONID=ABAAABAABEEAAJA1B1DFAE62C3164498D1AAA9F6FDFA840; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497678608; LGRID=20170617135014-d5c1980f-5320-11e7-9cd0-525400f775ce; TG-TRACK-CODE=index_search; LGSID=20170617134948-c5c76755-5320-11e7-9cd0-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D36.110.41.42',
		# ]

		self.headers = {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			"Referer": "https://www.lagou.com/jobs/list_%E4%B8%8A%E6%B5%B7%E5%BE%B7%E5%A8%81%E4%BC%81%E4%B8%9A%E5%8F%91%E5%B1%95%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8?city=%E4%B8%8A%E6%B5%B7&cl=true&fromSearch=true&labelWords=&suginput=",
			'User-Agent': self.ua.random,
			'X-Anit-Forge-Code': "0",
			'X-Anit-Forge-Token': "None",
			'X-Requested-With': "XMLHttpRequest",
			'Accept-Encoding': "gzip, deflate, br",
			# 'Cookie': random.choice(self.cookies)
		}
		# proxyMeta = "http://H4XGPM790E93518D:2835A47D56143D62@proxy.abuyun.com:9020"
		# self.proxies = {
		# 	"http": proxyMeta,
		# 	"https": proxyMeta,
		# }
		self.s = session()

	def get_json(self):
		"""
		第一台机器 id > 103859 and id <= 200000
		第二台机器 id > 311446 and id <= 400000
			第三台机器 id > 635353 and id <= 650000
			第四台机器 id > 889797 and id <= 900000
			第五台机器 id > 1135292 and id <= 1150000
			第六台机器 id > 1390295
		"""
		select_sql = "select id,quan_cheng from tyc_jichu_bj where id > 1413000"
		many = self.__db_handle(select_sql, type='select')
		for row in many:
			id = row['id']
			select_sql_has = """select id from tyc_jichu_bj_intro where id = %s"""
			args = (str(id),)
			id_list = self.__db_handle(select_sql_has, args=args, type='select')
			if len(id_list) == 1:
				print('exist id: ' + str(id))
				continue
			quan_cheng = row['quan_cheng']
			url = 'https://www.lagou.com/jobs/companyAjax.json'
			form_data = {'first': 'true', 'kd': '%s' % quan_cheng, 'pn': '1'}
			# 获取json
			response = self.__get_html(url, method='POST', form_data=form_data)
			# 超时
			if response == None:
				print('timeout: ' + str(id))
				self.__db_result(id, quan_cheng)
				continue
			time.sleep(random.randint(2, 4))

			json_dict = dict(json.loads(response.text))
			result = json_dict.get('content', {}).get('result', {})
			if result:
				companyId = result[0].get("companyId", 0)
				city = result[0].get("city", "")
				companyShortName = result[0].get("companyShortName", "")
				companyFullName = result[0].get("companyFullName", "")
				detail_url = 'https://www.lagou.com/gongsi/%d.html' % companyId
				# 获取简介
				response_detail = self.__get_html(detail_url, method='GET')

				if response_detail == None:
					print('timeout: ' + str(id))
					self.__db_result(id, quan_cheng)
					continue
				select = Selector(text=response_detail.text)
				desc_list = select.xpath('//span[@class="company_content"]//text()').extract()
				if len(desc_list) != 0:
					intro = ''.join([desc.strip() for desc in desc_list])
					insert_sql = """
						insert into tyc_jichu_bj_intro (id, quan_cheng, companyShortName, companyFullName, city, detail_url, intro) 
						VALUES (%s, %s, %s, %s, %s, %s, %s)
						ON DUPLICATE KEY UPDATE intro=VALUES(intro)
	                """
					args = (id, quan_cheng, companyShortName, companyFullName, city, detail_url, intro)
					is_ok = self.__db_handle(insert_sql, type='replace', args=args)
					if is_ok:
						print('intro insert success: ' + str(id))
						if id % 100 == 0:
							print(datetime.datetime.now())
					else:
						print('intro insert fail: ' + str(id))
				else:
					print('intro null: ' + str(id))
					self.__db_result(id, quan_cheng)
			else:
				print('no result: ' + str(id))
				self.__db_result(id, quan_cheng)

	def __db_result(self, id, quan_cheng):
		insert_sql_id = """
							insert into tyc_jichu_bj_intro (id, quan_cheng) 
							VALUES (%s, %s)
							ON DUPLICATE KEY UPDATE id=VALUES(id), quan_cheng=VALUES(quan_cheng)
		                """
		args = (id, quan_cheng)
		is_ok = self.__db_handle(insert_sql_id, type='replace', args=args)
		if is_ok:
			print('id insert success: ' + str(id))
			if id % 100 == 0:
				print(datetime.datetime.now())
		else:
			print('id insert fail: ' + str(id))

	def __get_html(self, url, method='GET', form_data=None, timeout=2):
		try:
			if method == 'GET':
				# response = self.s.get(url, headers=self.headers, proxies=self.proxies, timeout=timeout)
				response = self.s.get(url, headers=self.headers, timeout=timeout)
			elif method == 'POST':
				response = self.s.post(url, data=form_data, headers=self.headers, timeout=timeout)
		except requests.exceptions.ConnectTimeout:
			return None
		except requests.exceptions.Timeout:
			return None
		else:
			return response

	def __db_handle(self, my_sql, type='select', args=None):
		try:
			self.cursor.execute(my_sql, args)
			if type == 'select':
				result = self.cursor.fetchall()
				return result
			elif type == 'replace':
				self.conn.commit()
				return True
		except Exception as e:
			print(str(e))
			return False


def main():
	get_intro = GetIntro()
	# get_intro.get_json()
	# s = time.clock()
	p = Pool(processes=6)
	p.apply_async(get_intro.get_json())
	p.close()
	p.join()


# e = time.clock()
# print("time: {}".format(e - s))

if __name__ == '__main__':
	retry = 0
	while True:
		retry += 1
		try:
			main()
		except Exception as e:
			print('retry times: ' + str(retry))
			continue