# *-* coding: utf-8 *-*
import MySQLdb
import time
from datetime import datetime, timedelta
import json

db = None
cursor = None

def call_database():
	global db
	global cursor
	db = MySQLdb.connect(host="127.0.0.1", port=8889, user="root", passwd="root", db="roomify")
	cursor = db.cursor()
	return cursor

def hang_up_on_database():
	global db
	db = db.close()


def add_new_booking(date, int_val, location):
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
    cursor = call_database()
    global db
    sql="SELECT * FROM bookings WHERE DATE(date_booking) > CURDATE()"
    cursor.execute(sql)
    mighty_db_says = cursor.fetchall()
    hang_up_on_database()
    return mighty_db_says
