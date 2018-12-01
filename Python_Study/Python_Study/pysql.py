import pymysql

def insertSql(lst,conn):
	try:
		print("step9 : execute query")
		cur = conn.cursor()
		#cur.execute("select * from book_tb")
		sql = "insert into book_tb(isbn,title,book_location,nfc_id_fk,author,publisher) values (%s,%s,%s,%s,%s,%s)"
		cur.execute(sql,(lst[3],lst[0],'2','123456',lst[1],lst[2]))
		conn.commit()
		print("step10 : data in")
		#rows = cur.fetchall()
		#rows = list(rows)
		#for a in rows:
		#	print(a)
	except:
		print('Error')

if __name__ == '__main__':
	lst = ['title','author','pub','1251251']

	conn = pymysql.connect(
				user = 'grad',
				passwd = 'snrn132@',
				host = '49.236.137.29',
				port=3306,
				db='grad',
				charset='utf8')

	insertSql(lst,conn)

