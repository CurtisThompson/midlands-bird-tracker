from src.utils.extract_utils import request_page_soup, save_sightings_list, clean_sighting_text, clean_location_text


COUNTY = 'Derbyshire'
URL = 'https://www.derbyshireos.org.uk/news.php'
PARQUET_DIRECTORY = './data/scrape_extracts/'
PARQUET_NAME = 'dos'


def run(county=COUNTY, url=URL, file_name=PARQUET_NAME, file_directory=PARQUET_DIRECTORY):
    """Pull bird sightings from DOS website and store as parquet."""
    # Get URL soup
    soup = request_page_soup(url)

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
            try:
                location = li.find('strong').getText()
                birdtext = li.getText().replace(location, '')
                
                location = clean_location_text(location)
                birdtext = clean_sighting_text(birdtext)

                location_sightings.append([county, date, location, birdtext])
            except:
                print(f'Tuple extraction failed for {str(li)}')

    # Convert to dataframe and store
    save_sightings_list(location_sightings, file_directory, file_name)


if __name__ == "__main__":
    run()
