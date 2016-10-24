# *-* coding: utf-8 *-*
import requests
import base64
import json
import datetime

def post_speech(file_data):
    url = 'https://api.wit.ai/speech'
    file_dec = base64.b64decode(file_data[1])
    filename = 'new_sound.wav'
    with open(filename, 'wb') as f:
        f.write(file_dec)
    sound = open(filename, "rb")


    header ={
        'Authorization' : 'Bearer 2G6XUDBNKEWLFPJDLKEMTHEIHOSZG7HA',
        'Content-Type': 'audio/wav'
    }

    r = requests.post(url, data=sound, headers=header)
    sound.close()
    print r.content
    data = json.loads(r.content)
    error_list = content_parser(data)
    return {'errors':error_list, 'data':data}


def content_parser(data):
    error_list = []

    try:
         time = data['entities']['datetime'][0]['value']
    except KeyError:
        error_list.append('time')

    try:
        location = data['entities']['location'][0]['value'].lower()
        if location != 'niagara' or location != 'orkanen':
            error_list.append('location')
    except KeyError:
        error_list.append('location')

    return error_list



def time_master(req_time):
        time = req_time.time()
        int_time = int(str(time.strftime("%H")) + str(time.strftime("%M")))

        if int_time < 800:
            int_time = int_time + 1200

        elif int_time > 2000:
            int_time = int_time - 1200

        elif int_time >= 800 and int_time <= 815:
            int_time = 815


        time_slots = [
            [815,1000],
            [1001,1300],
            [1301,1500],
            [1501,1700],
            [1701,2000]
        ]

        prime_slot = "Out of range"
        sec_slot = None
        for idx, val in enumerate(time_slots):
            if int_time >= val[0] and int_time <= val[1]:
                prime_slot = idx
                if val[1] - int_time <= 50 and idx !=4:
                    prime_slot = idx+1
                    sec_slot = idx
                    break
                elif val[1] - int_time <= 100 and idx !=4:
                    sec_slot = idx+1
                    break

        return {'prime_slot':prime_slot,'sec_slot':sec_slot, 'time_slot_end':time_slots[prime_slot][1]}
