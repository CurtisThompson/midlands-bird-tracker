import requests
from bs4 import BeautifulSoup

URL = 'https://www.derbyshireos.org.uk/news.php'

# Request page contents
try:
    page = requests.get(URL).content
except:
    print('Failed to get DOS page content')

# Map to BeautifulSoup
soup = BeautifulSoup(page, features='lxml')

#birdnavdates = soup.find_all('div', {'id':'birdnavdate'})
birdnavs = [(d.getText(), d.find_next('ul', {'id':'birdnav'})) for d in soup.find_all('div', {'id':'birdnavdate'})]

for b in birdnavs:
    print(b[0])
    print(b[1])
    print()
    print()
    print()