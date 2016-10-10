
import requests
import json
from bs4 import BeautifulSoup
import re
import time

def book_room(s):
    rooms = get_rooms(s)
    

    book_room ={
        "op" : "boka",
        "datum" : '16-10-10',
        "id": 'NI:A0301',
        "typ" : 'RESURSER_LOKALER',
        "intervall": '4',
        "moment" : 'This room is Roomified',
        "flik" : "FLIK-0017"
    }

    booker = s.get('https://schema.mah.se/ajax/ajax_resursbokning.jsp', params = book_room)

    print booker.content
    return



def get_rooms(s):


    #0:'08:15-10:00'
    #1:'10:15-13:00'
    #2:'13:15-15:00'
    #3:'15:15-17:00'
    #4:'17:15-20:00'

    rooms = {
        '0':[],
        '1':[],
        '2':[],
        '3':[],
        '4':[]
    }

    houses =['FLIK-0017', 'FLIK_0000']

    date = (time.strftime("%y-%m-%d"))

    for house in houses:
        room_info = {
            "op" : "hamtaBokningar",
            "datum" : date,
            "flik" : house
        }

        headers = {
            'async': 'False',
            'content-type': 'application/json'
        }

        booker = s.get('https://schema.mah.se/ajax/ajax_resursbokning.jsp', params = room_info,  headers=headers)
        soup = BeautifulSoup(booker.content, 'lxml')
        mydivs = soup.findAll("td", { "class" : "grupprum-ledig" })

        for div in mydivs:
            link = div.find('a')
            if re.match('boka',link['onclick']):
                t = str(link['onclick'])
                sdata = t[t.find("(")+1:t.find(")")]
                new_data = sdata.split(',')
                x = [n.strip("'") for n in new_data]

                rooms[x[2]].append(x[0])

    return rooms










data = {
    'username': raw_input('Username:'),
    'password': raw_input('Password:')
}

head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
with requests.session() as s:
    resp = s.get('https://schema.mah.se')
    resp = s.post('https://schema.mah.se/login_do.jsp', data=data, headers=head)
    #resp = s.get('https://schema.mah.se/resursbokning.jsp?flik=FLIK-0017')
    #book_room(s)
    get_rooms(s)
