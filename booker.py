
import requests
#from bs4 import BeautifulSoup



data = {
    'username': raw_input('Username:'),
    'password': raw_input('Password:')
}

head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
with requests.session() as s:
    resp = s.get('https://schema.mah.se')
    resp = s.post('https://schema.mah.se/login_do.jsp', data=data, headers=head)
    resp = s.get('https://schema.mah.se/resursbokning.jsp?flik=FLIK-0017')


    print resp.content
