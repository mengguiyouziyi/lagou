import requests
import time
from bs4 import BeautifulSoup
import json


# url = 'http://app.mi.com/category/5#page=4'
# url = 'http://app.mi.com/categotyAllListApi?page=1&categoryId=5&pageSize=30'
urls = ['http://app.mi.com/categotyAllListApi?page=%d&categoryId=5&pageSize=30' % num for num in range(67)]
headers = {
	"Cookie":"""JSESSIONID=aaatWIRdp20blhyRvuaUv; __utma=127562001.1264147321.1497436570.1497436570.1497436570.1; __utmb=127562001.1.10.1497436570; __utmc=127562001; __utmz=127562001.1497436570.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)""",
	"Host":"app.mi.com",
	"Referer":"http://app.mi.com/category/5",
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
	"X-Requested-With":"XMLHttpRequest",
	"Connection":"keep-alive",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Accept-Encoding":"gzip, deflate",
	"Accept":"application/json, text/javascript, */*; q=0.01"
}
for url in urls:
	res = requests.get(url, headers=headers)
	print('sleep 2s ~~~~~')
	time.sleep(2)

