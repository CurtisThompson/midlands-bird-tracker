import logging

from bs4 import BeautifulSoup

from src.utils.extract_utils import request_page_soup, save_sightings_list, clean_sighting_text, clean_location_text


COUNTY = 'Nottinghamshire'
URL = 'https://www.nottsbirders.net/latest_sightings.html'
PARQUET_DIRECTORY = './data/scrape_extracts/'
PARQUET_NAME = 'notts'


def run(county=COUNTY, url=URL, file_name=PARQUET_NAME, file_directory=PARQUET_DIRECTORY):
    """Pull bird sightings from Notts website and store as parquet."""
    # Get URL soup
    soup = request_page_soup(url)

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
            logging.debug(f'Date extract failed: {str(extract)[50:]}...')


    # Split tuples into [date, location, bird text]
    location_sightings = []
    for birddate in date_bird_tuples:
        date = birddate[0]
        fulltext = BeautifulSoup(birddate[1], features='lxml')

        # Split location and text
        list_items = fulltext.find_all('p')
        for li in list_items:
            try:
                location = li.find('span').getText()
                birdtext = li.getText().replace(location, '')
                
                location = clean_location_text(location)
                birdtext = clean_sighting_text(birdtext)

                location_sightings.append([county, date, location, birdtext])
            except:
                logging.debug(f'Tuple extraction failed for {str(li)}')

    # Convert to dataframe and store
    save_sightings_list(location_sightings, file_directory, file_name)


if __name__ == "__main__":
    run()
