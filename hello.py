# *-* coding: utf-8 *-*

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, redirect
import requests
import base64
import wave

app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('index.html', name="Jacob")


@app.route('/data_sender', methods=['POST'])
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
		#'Content-Type': 'audio/mpeg3',
		'Content-Type': 'audio/wav'

	}

	r = requests.post(url, data=encoded_string, headers=header)
	print r.content
	return r.content


if __name__ == '__main__':
	app.run(debug=True)
