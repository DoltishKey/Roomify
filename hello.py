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

#from modules import booker
app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('index.html')


@app.route('/new_speech_request', methods=['POST'])
def handle_data():
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

	if 'location' in response['errors']:
		location = False
	else:
		return_response.append(response['data']['entities']['location'][0]['value'])


	if time == True:
		today = datetime.now()
		requested_time = str(response['data']['entities']['datetime'][0]['value'])
		timi = requested_time.split('.', 1 )
		req_time = datetime.strptime(timi[0], '%Y-%m-%dT%H:%M:%S')
		time_update = req_time + timedelta(hours=9)

		if today.date() == time_update.date():
			next_step = "Booker"
		else:
			date = req_time.date()
			next_step = "Core"

		book_time = witty.time_master(req_time)

	else:
		today = datetime.now()
		date = today.date()
		book_time = witty.time_master(today)


	time_respone = {
		'date':date,
		'primary_slot':book_time['prime_slot'],
		'sec_slot':book_time['sec_slot']
	}
	return_response.append(time_respone)


	return json.dumps(return_response)


@app.route('/new_text_request', methods=['POST'])
def send_text():
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
