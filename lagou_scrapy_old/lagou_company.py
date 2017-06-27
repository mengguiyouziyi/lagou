import requests

url = 'https://www.lagou.com/jobs/companyAjax.json'
headers = {
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"HOST": "www.lagou.com",
			"Referer": "https://www.lagou.com/jobs/list_%E4%B8%8A%E6%B5%B7%E5%BE%B7%E5%A8%81%E4%BC%81%E4%B8%9A%E5%8F%91%E5%B1%95%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8?city=%E4%B8%8A%E6%B5%B7&cl=true&fromSearch=true&labelWords=&suginput=",
			'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
			'X-Anit-Forge-Code': "0",
			'X-Anit-Forge-Token': "None",
			'X-Requested-With': "XMLHttpRequest",
			# 'Cookie': "user_trace_token=20170612170648-026cfbd0f39d4330b02cf404bac6d999; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497258409; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1497431940; LGRID=20170614171903-8241ec4c-50e2-11e7-9b3d-5254005c3644; LGUID=20170612170650-7898a127-4f4e-11e7-9ab4-5254005c3644; _ga=GA1.2.109776163.1497258409; JSESSIONID=ABAAABAABEEAAJAC9E004833C142BFC527E6D3D08485721; TG-TRACK-CODE=index_search; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.722219593.1497427964; LGSID=20170614161248-40ac1467-50d9-11e7-910b-525400f775ce; SEARCH_ID=59aa0b28d92045fab5b6507c86e33bee",
		}

meta = {'first':'true', 'kd':'上海德威企业发展股份有限公司', 'pn':'1', 'city':'上海'}


res = requests.post(url, headers=headers, data=meta)

pass
