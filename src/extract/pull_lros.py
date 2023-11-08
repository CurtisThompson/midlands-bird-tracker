import requests
from bs4 import BeautifulSoup
import polars as pl

COUNTY = 'Leicestershire'
URL = 'https://lros.org.uk/sightings-records/latest-bird-news/'

# Request page contents
try:
    page = requests.get(URL).content
except:
    print('Failed to get LROS page content')

# Map to BeautifulSoup
soup = BeautifulSoup(page, features='lxml')

# Get bird reports section of contents, split by date
articles = soup.find_all('article')[1:]
date_bird_tuples = []
for a in articles:
    # Get inner content
    content = a.find('div', {'class':'et_pb_text_inner'})
    content = str(content)

    # Find each date and extract text
    date_texts = content.split('<h4>')[1:]
    for extract in date_texts:
        try:
            parts = extract.split('</h4>')
            extract_date = parts[0].strip()
            extract_birds = parts[1].strip()
            date_bird_tuples.append((extract_date, extract_birds))
        except:
            print(f'Date extract failed: {str(extract)[50:]}...')


# Split tuples into [date, location, bird text]
location_sightings = []
for birddate in date_bird_tuples:
    date = birddate[0]
    fulltext = BeautifulSoup(birddate[1], features='lxml')

    # Split location and text
    list_items = fulltext.find_all('p')
    for li in list_items:
        try:
            location = li.find('em').getText()
            birdtext = li.getText().replace(location, '').strip()
            if birdtext.startswith('- ') or birdtext.startswith(': '):
                birdtext = birdtext[2:].strip()
            location = location.strip()
            location_sightings.append([COUNTY, date, location, birdtext])
        except:
            print(f'Tuple extraction failed for {str(li)}')

# Convert to dataframe and store
df = pl.DataFrame(location_sightings, orient='row')
df.columns = ['County', 'Date', 'Location', 'BirdText']
df.write_parquet('./data/scrape_extracts/lros.parquet')