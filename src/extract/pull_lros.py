import logging

from bs4 import BeautifulSoup

from src.utils.extract_utils import request_page_soup, save_sightings_list, clean_sighting_text, clean_location_text


COUNTY = 'Leicestershire'
URL = 'https://lros.org.uk/sightings-records/latest-bird-news/'
PARQUET_DIRECTORY = './data/scrape_extracts/'
PARQUET_NAME = 'lros'


def run(county=COUNTY, url=URL, file_name=PARQUET_NAME, file_directory=PARQUET_DIRECTORY):
    """Pull bird sightings from LROS website and store as parquet."""
    # Get URL soup
    soup = request_page_soup(url)
    if soup is None:
        return None

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
                location = li.find('em').getText()
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
