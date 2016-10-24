
import requests
import json
from bs4 import BeautifulSoup
import re
import time
import datetime
import core


def book_room(int_val, location):
    s = login()
    rooms = get_rooms(s)
    try:
        room = rooms[str(int_val)][0]

    except IndexError:
        return {'result':'False'}

    if location == 'Niagara':
        flik = "FLIK-0017"
    else:
        flik= "FLIK_0000"

    date = time.strftime("%y-%m-%d")

    book_room ={
        "op" : "boka",
        "datum" : date,
        "id": room,
        "typ" : 'RESURSER_LOKALER',
        "intervall": int_val,
        "moment" : 'This room is Roomified',
        "flik" : flik
    }
    booker = s.get('https://schema.mah.se/ajax/ajax_resursbokning.jsp', params = book_room)


    if booker.content == 'OK':
        return {'result':'True'}
    else:
        return  {'result':'False'}


def myBookings():
    s = login()
    date = time.strftime("%y-%m-%d")
    fliks = ["FLIK-0017", "FLIK_0000"]
    book_info = []

    for flik in fliks:
        get_room ={
            "datum" : date,
            "flik" : flik
        }
        bookings = s.get('https://schema.mah.se/minaresursbokningar.jsp', params = get_room)
        soup = BeautifulSoup(bookings.content, "html.parser")
        parent = soup.find('div', id="minabokningar")
        for tag in parent.find_all(class_="ui-widget-content ui-corner-all"):
            room = {}
            booking_id_list = tag.get('id').split('_', 1)
            room['book_id'] = booking_id_list[1]


            data = tag.find('div').text.split(' ')
            room['start'] = data[1]

            room['room'] = tag.find('b').text.split(',')[1]
            book_info.append(room)

    book_info = sorted(book_info, key=lambda k: k['start'])

    return book_info

def removeBooking(id):
    s = login()
    delte_room ={
        "op" : 'avboka',
        "bokningsId" : id
    }
    bookings = s.get('https://schema.mah.se/ajax/ajax_resursbokning.jsp', params = delte_room)
    print bookings.content

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
        soup = BeautifulSoup(booker.content, "html.parser")
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

def test_booking(inpat):
    print inpat['date']
    print inpat['time']
    print inpat['location']




def login():
    data = {
        'username': 'ac8240',
        'password': '92F39gb2'
    }
    head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    with requests.session() as s:
        resp = s.get('https://schema.mah.se')
        resp = s.post('https://schema.mah.se/login_do.jsp', data=data, headers=head)
        return s

myBookings()
