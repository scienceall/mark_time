import sqlite3
import time
import datetime
import inspect
con = sqlite3.connect('work_since_12.05.2020')
c = con.cursor()

def read_from_database_normal():
	c.execute('select * from working')
	for row in c.fetchall():
		print (datetime.datetime.fromtimestamp(row[0]).strftime('%d.%m.%Y %H:%M:%S'), end = '')
		print (datetime.datetime.fromtimestamp(row[1]).strftime(' - %d.%m.%Y %H:%M:%S'))
		print ('')



def read_from_database_unix():
	c.execute('select * from working')
	for row in c.fetchall():
		print (row)


def show_all():
	read_from_database_normal()
	print('.....')
	read_from_database_unix()





def check_if_1st_rec_not_finished():
	c.execute('select max(end_time) from working')
	find_max_val = c.fetchone()[0]
	wont_be_used_var = 1 / find_max_val


show_all()
