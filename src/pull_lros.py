import requests
from bs4 import BeautifulSoup

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
            extract_date = parts[0]
            extract_birds = parts[1]
            date_bird_tuples.append((extract_date, extract_birds))
        except:
            print(f'Date extract failed: {str(extract)[50:]}...')


for a in date_bird_tuples:
    print(a[0])
    print(a[1])
    print()
    print()
    print()
    print()