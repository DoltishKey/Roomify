# *-* coding: utf-8 *-*
import MySQLdb
import booker
from datetime import datetime
from threading import Timer


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

x=datetime.today()
y=x.replace(day=x.day+1, hour=0, minute=0, second=0, microsecond=0)
delta_t=y-x
secs=delta_t.seconds+1

t = Timer(secs, do_booking)
t.start()
