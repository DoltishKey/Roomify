# *-* coding: utf-8 *-*
#Program (för framtiden) som ska köras på Raspberry Pi varje natt för att utför alla bokningar i pipen.
import MySQLdb
import booker
from datetime import datetime
import schedule
import time
db = None
cursor = None

def call_database():
'''
	*--Kopplar upp mot databsen och skapar ett cursor-objekt.--*
'''
	global db
	global cursor
	db = MySQLdb.connect(host="127.0.0.1", port=8889, user="root", passwd="root", db="roomify")
	cursor = db.cursor()
	return cursor

def hang_up_on_database():
	'''
		*--Kopplar ned anslutnigne mot databsen.--*
	'''
	global db
	db = db.close()

def get_todays_batch():
	'''
		*--Hämtar alla boknignar som ska göra samma datum.--*
	'''
    cursor = call_database()
    sql = "SELECT time_slot, location FROM bookings WHERE DATE(date_booking) = CURDATE()"
    cursor.execute(sql)
    mighty_db_says = cursor.fetchall()
    hang_up_on_database()
    return mighty_db_says


def do_booking():
	'''
		*--Utför alla boknignar.--*
	'''
    batch = get_todays_batch()
    for item in batch:
        booker.book_room(item[0],item[1])


#Timer som ser till att scriptet körs varje natt. 
schedule.every().day.at("00:00").do(do_booking)
while 1:
    schedule.run_pending()
    time.sleep(1)
