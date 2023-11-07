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

print(soup)