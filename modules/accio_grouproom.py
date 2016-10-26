# *-* coding: utf-8 *-*
import requests
import time
'''
    OBS! Avbokar alla bokningar som finns för alla användare på hela Malmö Högskola på dagens datum
'''
def createChaoos():
    s = login()
    start = 001
    while start <= 817:
        date = time.strftime("%Y%m%d")
        if start < 10:
            num = '00'+str(start)
        elif start < 100 and start >= 10:
            num = '0'+str(start)
        else:
            num = str(start)

        id_remove = 'BokningsId_' + date + '_000000'+ str(num)
        removeBooking(s, id_remove)
        start = start + 2



def removeBooking(s, id):
    #Avboka ett grupprum, baserat på bokningsId
    delte_room ={
        "op" : 'avboka',
        "bokningsId" : id
    }
    bookings = s.get('https://schema.mah.se/ajax/ajax_resursbokning.jsp', params = delte_room)
    print bookings.content
    return


def login():
    #logga in med personliga inloggningsuppgifter för att få tillgång till kronox
    data = {
        'username': 'your_username',
        'password': 'your_password'
    }
    head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    with requests.session() as s:
        resp = s.get('https://schema.mah.se')
        resp = s.post('https://schema.mah.se/login_do.jsp', data=data, headers=head)
        return s

createChaoos()
