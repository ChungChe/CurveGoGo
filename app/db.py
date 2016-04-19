import sqlite3 as db
import sys
import time
import random

dbName = "curve.db"

def create_db(dbName):
	try:
		con = db.connect(dbName)
		cur = con.cursor()
		cur.execute("create table a_curve ( \
					machine_id INTEGER not null, \
					value REAL, \
					timestamp DATETIME default CURRENT_TIMESTAMP \
				)")
		con.commit()
	except db.Error, e:
		if con:
			con.rollback()
		print("Error %s:" % e.args[0])
		sys.exit(1)
	finally:
		if con:
			con.close()

def insert(cur, m_id, value):
	data = [m_id, value]
	cur.execute("insert into a_curve values (?,?,datetime('now'))", data)

def get_data(cur, start, end, machinelist):
	st = "(" + ",".join(["?"] * len(machinelist)) + ")"
	print("machine: " + str(machinelist) + " between " + start + " and " + end)
	input_list = [start, end] + machinelist
	cur.execute("select * from a_curve where timestamp between ? and ? and machine_id in " + st, input_list)
	outputList = cur.fetchall()
	for element in outputList:
		print(element)

def random_insert(con, cur):
		for i in range(200): 
			wait_s = random.randint(1, 4)
			time.sleep(wait_s);
			m_id = random.randint(1, 25)
			v = random.uniform(50, 150)
			print('id: ' + str(m_id) + ', value: ' + str(v))
			insert(cur, m_id, v)
		con.commit()

def main():
	try:
		con = db.connect('curve.db')
		print('Connect to curve.db')
		cur = con.cursor()
		machine_list = [22, 2, 5, 8]
		get_data(cur, '2016-04-18 12:42:53', '2016-04-18 16:43:07', machine_list)
	except db.Error, e:
		if con:
			con.rollback()
		print("Error %s" % e.args[0])
		sys.exit(1)
	finally:
		if cur:
			cur.close()
		if con:
			con.close()
	
#create_db(dbName)
main()
