# *-* coding:utf-8 *-*
#Need to instal selenium and PhantomJS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from threading import Timer

def welcome():
    pass

def send_confirmation():
    pass

def run_timer():
    today = datetime.today()
    nextday = today.replace(day=today.day+1, hour=0, minute=0, second=0, microsecond=1)
    delta_time = nextday - today
    secs = delta_time.seconds + 1
    t = Timer(secs, scraper)
    t.start()
    #run_timer()


def login(username, password):
    driver = webdriver.PhantomJS()
    driver.get('https://schema.mah.se')

    #Opens sigin-menu
    bt = driver.find_element_by_class_name('signin')
    bt.click()

    #Sets username
    u = driver.find_element_by_id('login_username')
    u.send_keys(username)

    #Sets password
    p = driver.find_element_by_id('login_password')
    p.send_keys(password)

    #Hits login
    login_form = driver.find_element_by_id('loginform')
    login_form.submit()

    return driver

def logout(driver):
    nav = driver.find_element_by_id('topnav')
    logout_btn = nav.find_element_by_class_name('greenbutton')
    logout_btn.click()

    driver.close()


def scraper():
    driver= login('userName', 'password')


    # 1. Niagara
    # 2. Orkanen
    # Order in prefered way
    houses=[
        'https://schema.mah.se/resursbokning.jsp?flik=FLIK-0017',
        'https://schema.mah.se/resursbokning.jsp?flik=FLIK_0000'
    ]

    times={
        '08:15 - 10:00' : 1,
        '10:15 - 13:00' : 2,
        '13:15 - 15:00' : 3,
        '15:15 - 17:00' : 4,
        '17:15 - 20:00' : 5,
    }
    room_is_roomified = False

    #for key, value in houses.iteritems():
    for key in houses:
        print key
        #driver.get(value)
        driver.get(key)
        all_rooms = driver.find_element_by_class_name('grupprum-table')
        rooms = all_rooms.find_elements_by_tag_name('tr')
        for room in rooms[1:]:
            bookables = room.find_elements_by_tag_name('td')

            #Update time for prefered time - see dict times
            to_book = bookables[times['13:15 - 15:00']]
            if 'grupprum-ledig' in to_book.get_attribute('outerHTML'):
                bookLink = to_book.find_element_by_class_name('tooltip')
                bookLink.click()

                #Sets moment
                moment = driver.find_element_by_id('moment')
                moment.send_keys('This room is now Roomified!')
                box = driver.find_element_by_xpath("//*[@aria-labelledby='ui-dialog-title-boka-dialog']")
                buttons = box.find_elements_by_tag_name('button')
                buttons[1].click()
                room_is_roomified = True
                print 'Room is now Roomified'
                break

        if room_is_roomified == True:
            break

    if room_is_roomified == False:
        print 'No room aviable'

    logout(driver)

run_timer()
#scraper()
