# *-* coding: utf-8 *-*
import MySQLdb
import time
from datetime import datetime, timedelta
import json

db = None
cursor = None

def call_database():
	#Skapar en uppkoppling till databas
	global db
	global cursor
	db = MySQLdb.connect(host="127.0.0.1", port=8889, user="root", passwd="root", db="roomify")
	cursor = db.cursor()
	return cursor

def hang_up_on_database():
	#Stänger ner uppkopplingen till databas
	global db
	db = db.close()


def add_new_booking(date, int_val, location):
	#Lägg in ny bokning i databas
    cursor = call_database()
    global db
    sql = "INSERT INTO bookings(date_booking, time_slot, location)\
    VALUES(%s,%s,%s )"
    cursor.execute(sql,(date,int_val,location,))
    last_id = cursor.lastrowid
    db.commit()
    hang_up_on_database()
    return last_id

def get_my_bookings():
	#Hämta alla mina bokningar i databas
	cursor = call_database()
	global db
	sql="SELECT * FROM bookings WHERE DATE(date_booking) > CURDATE() ORDER BY date_booking, time_slot"
	cursor.execute(sql)
	mighty_db_says = cursor.fetchall()
	hang_up_on_database()
	mighty_db_says = list(mighty_db_says)
	for idx, item in enumerate(mighty_db_says):
		mighty_db_says[idx] = list(item)
		mighty_db_says[idx][1] = item[1].strftime('%Y-%m-%d')

	return mighty_db_says


def removeBooking(id_remove):
	#Avboka en inlagd bokning i databasen
	id_remove = int(id_remove)
	print type(id_remove)
	cursor = call_database()
	global db
	sql = "DELETE FROM bookings WHERE id = %s"
	cursor.execute(sql, (id_remove,))
	db.commit()
	hang_up_on_database()
	return
