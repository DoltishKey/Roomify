# *-* coding: utf-8 *-*
import MySQLdb
import booker
from datetime import datetime
import schedule
import time



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

def get_todays_batch():
    cursor = call_database()
    sql = "SELECT time_slot, location FROM bookings WHERE DATE(date_booking) = CURDATE()"
    cursor.execute(sql)
    mighty_db_says = cursor.fetchall()
    hang_up_on_database()
    return mighty_db_says


def do_booking():
    batch = get_todays_batch()
    for item in batch:
        booker.book_room(item[0],item[1])

schedule.every().day.at("00:00").do(do_booking)

while 1:
    schedule.run_pending()
    time.sleep(1)
