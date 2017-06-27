__author__ = 'Administrator'

import pymysql
import json

mysql = pymysql.connect(
	host='101.200.166.12',
	user='spider',
	password='spider',
	db='spider',
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor,
	use_unicode=True
)


def get(key, value):
	try:
		return key[value]
	except Exception as e:
		return ''


def Jiexi():
	with mysql.cursor() as cursor:
		sql1 = "select t_id,leading_member,shareholder_Information,outbound_investment from tyc_information limit 10"
		sql2 = "insert into tyc_company_employee1(com_id,per_name,per_position) values(%s,%s,%s)"
		sql3 = "insert into tyc_company_shareholder(com_id,shareholder_name,contribution_amount,contribution_rate) values(%s,%s,%s,%s)"
		sql4 = "insert into tyc_company_out_investment(com_id,invest_name,representative,register_amount,register_date,scope_business,investment_amount,investment_rate,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql1)
		result = cursor.fetchall()
		mysql.commit()
		print(result)
		page = 0
		for i in result:
			try:
				zhuyao = get(i, 'leading_member')
				gudong = get(i, 'shareholder_Information')
				duiwai = get(i, 'outbound_investment')
				tid = get(i, 't_id')
				break
				if zhuyao is not None:
					a = json.loads(zhuyao)
					for aa in a:
						cursor.execute(sql2, (tid, get(aa, 'ming'), get(aa, 'zhiwu')))
						mysql.commit()
				if gudong is not None:
					b = json.loads(gudong)
					for bb in b:
						cursor.execute(sql3, (tid, get(bb, 'ming'), get(bb, 'renjiaochuzi'), get(bb, 'chuzibili')))
						mysql.commit()
				if duiwai is not None:
					c = json.loads(duiwai)
					for cc in c:
						cursor.execute(sql4, (
							tid, get(cc, 'beitouziqiyemingcheng'), get(cc, 'fadingdaibiaoren'), get(cc, 'zhuceziben'),
							get(cc, 'zhuceshijian'), get(cc, 'jingyingfanwei'), get(cc, 'touzishue'),
							get(cc, 'touzizhanbi'), get(cc, 'zhuangtai')))
						mysql.commit()
				page = page + 1
				print(page)
			except Exception as e1:
				print('error' + '     ' + e1.message)


if __name__ == '__main__':
	Jiexi()
