# *-* coding: utf-8 *-*

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, redirect
import requests
import base64
import wave
from modules import core
from modules import witty
import json
import time
from datetime import datetime, timedelta
from modules import booker
from modules import core

''' Hello.py är servern vars roomify körs'''

app = Flask(__name__)

@app.route('/')
def welcome():
	# På URL '/' renderas en html-fil som "startsida" för roomify
	return render_template('index.html')


@app.route('/new_speech_request', methods=['POST'])
def handle_data():
	# Läser in ljudfil, konverteras till b64-format
	# Skickar datan till wit.ai som tolkar ljudfilen och returnerar den data som kunde utläsas
	# Returnerar en lista av fel ifall sådanna uppkom.
	# Hanterar formateringen av datum/tid baserat på data som genererats av wit.ai
	# Om dagens datum ---> boka grupprum direkt.
	# Om annat än dagens datum ---> lägg in bokning i databas
	# Genererades ingen datum/tid från wit.ai: utgå från dagens datum och nuvarande tid
	# Lägg till datum/tid för bokning i listan för bokningar
	# Returnera data till front-end
	in_data = request.form

	file_in = base64.b64decode(in_data['sound'])
	file_data = file_in.split(',', 1 )
	response = witty.post_speech(file_data)
	return_response=[
		{'errors':response['errors']}
	]

	time = True
	location = True

	if 'time' in response['errors']:
		time = False

	if time == True:
		today = datetime.now()
		requested_time = str(response['data']['entities']['datetime'][0]['value'])
		timi = requested_time.split('.', 1 )
		req_time = datetime.strptime(timi[0], '%Y-%m-%dT%H:%M:%S')
		time_update = req_time + timedelta(hours=9)
		book_time = witty.time_master(req_time)

		if today.date() == time_update.date():
			next_step = "Booker"
			date = today.date()
			time_now=int(str(today.strftime("%H")) + str(today.strftime("%M")))
			if time_now > book_time['time_slot_end'] and book_time['prime_slot'] == 4:
				date = date + timedelta(days=1)
			elif time_now > book_time['time_slot_end'] and book_time['prime_slot'] != 4:
				book_time = witty.time_master(today)

		else:
			date = req_time.date()
			next_step = "Core"

	else:
		today = datetime.now()
		date = today.date()
		book_time = witty.time_master(today)

	time_respone = {
		'date':str(date),
		'primary_slot':book_time['prime_slot'],
		'sec_slot':book_time['sec_slot']
	}
	return_response.append(time_respone)


	if 'location' in response['errors']:
		location = False
	else:
		return_response[1]['location'] = response['data']['entities']['location'][0]['value']

	return json.dumps(return_response)

@app.route('/grouprooms', methods=['POST'])
def grouprooms():
	#Utför grupprumsbokning
	in_data = request.form
	in_time = in_data['time']
	location = in_data['location']
	date = in_data['date']
	con_date = datetime.strptime(date,'%Y-%m-%d')
	today_date = datetime.now()

	if con_date.date() == today_date.date():
		res=booker.book_room(in_time,location)
		if res['result'] == 'True':
			core.add_new_booking(con_date.date(), int(in_time), location)
			return 'OK'
		else:
			return 'No available room'

	else:
		core.add_new_booking(con_date.date(), int(in_time), location)
		return 'OK'

@app.route('/grouprooms', methods=['GET'])
def get_grouprooms():
	#hämta mina bokningar som är sparade i databasen
	bookings=core.get_my_bookings()
	return json.dumps(bookings)

@app.route('/room_today', methods=['GET'])
def get_room_today():
	#hämta mina bokningar som är genomförda i kronox
	bookings=booker.myBookings()
	return json.dumps(bookings)

@app.route('/grouprooms', methods=['DELETE'])
def delete_grouprooms():
	#Avboka bokade grupprum i databasen
	in_data = request.form
	id_remove=in_data['id']
	core.removeBooking(id_remove)
	return 'OK'

@app.route('/room_today', methods=['DELETE'])
def delete_room_today():
	#Avboka bokade grupprum som bokats på Kronox
	in_data = request.form
	book_id = in_data['id']
	booker.removeBooking(book_id)
	return 'OK'


@app.route('/new_text_request', methods=['POST'])
def send_text():
	#Om mic ej fungerar - så kan användaren lägga in en bokning i form av text_request
	#Under construction
	in_data = request.form
	to_do = in_data['text_request']
	print to_do
	url = 'https://api.wit.ai/message'
	data = {
		'access_token' : '2G6XUDBNKEWLFPJDLKEMTHEIHOSZG7HA',
		'q': to_do
	}
	r = requests.get(url, params = data)
	return r.content



if __name__ == '__main__':
	app.run(debug=True)
