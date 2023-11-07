import requests
from bs4 import BeautifulSoup

URL = 'https://www.nottsbirders.net/latest_sightings.html'

# Request page contents
try:
    page = requests.get(URL).content
except:
    print('Failed to get Notts page content')

# Map to BeautifulSoup
soup = BeautifulSoup(page, features='lxml')

# Extract main content
content = soup.find('div', {'id':'main_content'})
content = str(content)

# Split into dates
date_bird_tuples = []
date_texts = content.split('<h2 class="main_content_title">')[1:]
for extract in date_texts:
    try:
        parts = extract.split('</h2>')
        extract_date = parts[0].strip()
        extract_birds = parts[1].strip()

        # Remove footer from birds text
        if '<hr/>' in extract_birds:
            extract_birds = extract_birds.split('<hr/>')[0]

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
        location = li.find('span').getText()
        birdtext = li.getText().replace(location, '').strip()
        if birdtext.startswith('- ') or birdtext.startswith(': '):
            birdtext = birdtext[2:].strip()
        location = location.strip()
        location_sightings.append([date, location, birdtext])
        print([date, location, birdtext])