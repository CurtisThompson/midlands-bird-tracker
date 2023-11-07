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


for a in date_bird_tuples:
    print(a[0])
    print(a[1])
    print()
    print()
    print()
    print()