
import requests
import json
#from bs4 import BeautifulSoup



data = {
    'username': raw_input('Username:'),
    'password': raw_input('Password:')
}

head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
with requests.session() as s:
    resp = s.get('https://schema.mah.se')
    resp = s.post('https://schema.mah.se/login_do.jsp', data=data, headers=head)
    #resp = s.get('https://schema.mah.se/resursbokning.jsp?flik=FLIK-0017')

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



def get_rooms():
    room_info = {
        "op" : "hamtaBokningar",
        "datum" : "16-10-10",
        "flik" : "FLIK-0017"
    }

    headers = {
        'async': 'False'
    }

    booker = s.get('https://schema.mah.se/ajax/ajax_resursbokning.jsp', params = room_info,  headers=headers)
    print booker.url

    print booker.content
