import requests
from bs4 import BeautifulSoup
import polars as pl

COUNTY = 'Derbyshire'
URL = 'https://www.derbyshireos.org.uk/news.php'

# Request page contents
try:
    page = requests.get(URL).content
except:
    print('Failed to get DOS page content')

# Map to BeautifulSoup
soup = BeautifulSoup(page, features='lxml')

# Extract tuple of dates and bird text
birdnavs = [(d.getText(), d.find_next('ul', {'id':'birdnav'})) for d in soup.find_all('div', {'id':'birdnavdate'})]

# Split tuples into [date, location, bird text]
location_sightings = []
for birddate in birdnavs:
    date = birddate[0]
    fulltext = birddate[1]

    # Split location and text
    list_items = fulltext.find_all('li')
    for li in list_items:
        location = li.find('strong').getText()
        birdtext = li.getText().replace(location, '').strip()
        location = location.strip()
        if (location[-8] == '(') and (location[-1] == ')'):
            location = location[:-9]
        location_sightings.append([COUNTY, date, location, birdtext])
        print([date, location, birdtext])

# Convert to dataframe and store
df = pl.DataFrame(location_sightings, orient='row')
df.columns = ['County', 'Date', 'Location', 'BirdText']
df.write_parquet('./data/scrape_extracts/dos.parquet')