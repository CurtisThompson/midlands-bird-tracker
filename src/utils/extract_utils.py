import os
import requests
from bs4 import BeautifulSoup
import polars as pl


def request_page_soup(url):
    """Requests URL page contents and wraps in BeautifulSoup."""    
    try:
        # Request page contents
        page = requests.get(url).content
        # Map to BeautifulSoup
        soup = BeautifulSoup(page, features='lxml')
        return soup
    except:
        print(f'Failed to get {url} page content')
        return None


def clean_location_text(text):
    """Cleans location text of whitespace and unneeded characters."""
    text = text.strip()

    if (text[-8] == '(') and (text[-1] == ')'):
        text = text[:-9].strip()
    
    return text


def clean_sighting_text(text):
    """Cleans sighting text of whitespace and unneeded characters."""
    text = text.strip()

    if text.startswith('- ') or text.startswith(': '):
        text = text[2:].strip()
    
    return text


def save_sightings_list(sightings, directory, file_name):
    """Takes a list of (County, Date, Location, Sightings) and saves parquet."""
    df = pl.DataFrame(sightings, orient='row')
    df.columns = ['County', 'Date', 'Location', 'BirdText']
    path = os.path.join(directory, f'{file_name}.parquet')
    df.write_parquet(path)