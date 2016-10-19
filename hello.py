# *-* coding: utf-8 *-*

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, redirect
import requests
import base64
import wave

app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('index.html')


@app.route('/new_speech_request', methods=['POST'])
def handle_data():
	in_data = request.form


	url = 'https://api.wit.ai/speech'
	file_in = base64.b64decode(in_data['sound'])
	file_data = file_in.split(',', 1 )
	file_dec = base64.b64decode(file_data[1])
	filename = 'new_sound.wav'
	with open(filename, 'wb') as f:
		f.write(file_dec)
	sound = open(filename, "rb")
	encoded_string = sound
	header ={
		'Authorization' : 'Bearer 2G6XUDBNKEWLFPJDLKEMTHEIHOSZG7HA',
		'Content-Type': 'audio/wav'
	}

	r = requests.post(url, data=encoded_string, headers=header)
	print r.content
	return r.content


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
