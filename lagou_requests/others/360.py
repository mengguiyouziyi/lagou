import requests

try:
	import cookielib
except:
	import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
	session.cookies.load(ignore_discard=True)
except:
	print("cookie未能加载")

proxyMeta = "http://H4XGPM790E93518D:2835A47D56143D62@proxy.abuyun.com:9020"
proxies = {
	"http": proxyMeta,
	"https": proxyMeta,
}

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	# 'Accept-Encoding': "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	# "Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	# "HOST": "trends.so.com",
	# "HOST": "i.360.cn",
	"Upgrade-Insecure-Requests": "1",
	'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
}


def login(acount=None, password=None):
	# url = 'http://i.360.cn/login/'
	url = 'https://login.360.cn/'
	post_data = {
		# "_xsrf": get_xsrf(),
		# "phone_num": acount,
		# "password": password,
		# "captcha":get_captcha()
		"src": "pcw_360index",
		"from": "pcw_360index",
		"charset": "UTF-8",
		"requestScema": "https",
		"o": "sso",
		"m": "login",
		"lm": "0",
		"captFlag": "1",
		"rtype": "data",
		"validatelm": "0",
		"isKeepAlive": "1",
		"captchaApp": "i360",
		"userName": "13784855457",
		"type": "normal",
		"account": "13784855457",
		"password": "855a4fe7c57308da4f77015ac6db6937",
		# "captcha": "hsrrx",
		"token": "8b7e95ce3a510603",
		"proxy": "http%3A%2F%2Ftrends.so.com%2Fpsp_jump.html",
		"callback": "QiUserJsonp318626729",
		"func": "QiUserJsonp318626729"

	}
	headers.update({
		"HOST": "login.360.cn",
		"Referer": "http://trends.so.com/index",
		'Accept-Encoding': "gzip, deflate, br",
	})
	response = session.request('POST', url, headers=headers, data=post_data, proxies=proxies)
	with open('u.html', 'w') as f:
		f.write(response.text)
	session.cookies.save()


def get_captcha():
	import time
	t = str(int(time.time() * 1000))
	"https://passport.360.cn/captcha.php?m=create&app=i360&scene=login&userip=nWE5SCVWNwncWWY6UXNudg%3D%3D&level=default&sign=69e32f&r=1499320329&_=1499320330472"
	captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
	t = session.get(captcha_url, headers=headers)
	with open("captcha.jpg", "wb") as f:
		f.write(t.content)
		f.close()

	from PIL import Image
	try:
		im = Image.open('captcha.jpg')
		im.show()
		im.close()
	except:
		pass

	captcha = input("输入验证码\n>")
	return captcha


def is_login():
	headers.update({
		"HOST": "trends.so.com",
	})
	url = 'http://trends.so.com/index'
	response = session.request('GET', url, headers=headers)
	print(response.text)


if __name__ == '__main__':
	login(13784855457, 3646287)
# is_login()
