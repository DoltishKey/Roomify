
import requests
import base64
import argparse
import json



def test_two():

    #handling = raw_input('What do you want to do?')
    url = 'https://api.wit.ai/message'
    data = {
        'access_token' : '2G6XUDBNKEWLFPJDLKEMTHEIHOSZG7HA',
        'q': 'Book a room tomorrow at 2 in Niagara'
    }

    r = requests.get(url, params = data)

    print r.content




def req():

    url = 'https://api.wit.ai/speech'
    encoded_string = open("booka.mp3", "rb")
    header ={
        'Authorization' : 'Bearer 2G6XUDBNKEWLFPJDLKEMTHEIHOSZG7HA',
        'Content-Type': 'audio/mpeg3',
    }

    r = requests.post(url, data=encoded_string, headers=header)

    print r.content


def google_speech():

    url='https://speech.googleapis.com/'
    url = 'https://speech.googleapis.com/v1beta1/speech:AIzaSyCM2HeWc_6cphgBbMlCx8Gbw-gmPQOTsfw'
    audio = open('booka.flac', 'rb')
    encoded_audio = base64.b64encode(audio.read())
    header = {

        'encoding':'FLAC',
        'sampleRate':16000,
        'languageCode':'en-US'
      }

    r = requests.post(url, data=encoded_audio, headers=header)
    print r.content



google_speech()
#req()
