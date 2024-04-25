import polars as pl
from geopy.geocoders import Nominatim
from time import sleep
from random import random
import dateutil.parser as dateparser
import datetime


COORDINATE_API_USER_AGENT = 'midlands-bird-tracker'
CACHED_COORDINATE_FILE = './data/location_coordinates.parquet'
OUTPUT_FILE = './data/bird_sightings.parquet'
SCRAPED_FILES = ['./data/scrape_extracts/dos.parquet',
                 './data/scrape_extracts/lros.parquet',
                 './data/scrape_extracts/notts.parquet']


def get_location_coordinates(location, user_agent=COORDINATE_API_USER_AGENT):
    """Retrieve coordinates of string-based location using API."""
    try:
        geolocator = Nominatim(user_agent=user_agent)
        loc = geolocator.geocode(location)
        sleep(random())
        return {'Latitude':loc.latitude, 'Longitude':loc.longitude}
    except:
        return {'Latitude':0.0, 'Longitude':0.0}


def add_location_coordinates_column(df, cache_file=CACHED_COORDINATE_FILE):
    """Add latitude and longitude columns from string-based location column."""
    # Get dataframe of unique locations
    df_loc = df.unique('FullLocation').select('FullLocation')

    # Load existing locations
    df_loc_existing = pl.read_parquet(cache_file)

    # Join coordinates to unique locations
    df_loc = df_loc.join(df_loc_existing, on='FullLocation', how='left').fill_null(0.0)

    # Find all locations without proper coordinates
    df_loc_missing = df_loc.filter((pl.col('Latitude') == 0)
                                & (pl.col('Longitude') == 0))
    df_loc_missing = df_loc_missing.select('FullLocation')

    # Attempt to find latitude and longitude of missing locations
    df_loc_missing = df_loc_missing.with_columns(pl.col('FullLocation')
                                                .apply(get_location_coordinates)
                                                .alias('Coordinates'))
    df_loc_missing = df_loc_missing.unnest('Coordinates')

    # Save new found coordinates
    df_loc_missing = df_loc_missing.filter((pl.col('Latitude') != 0)
                                        & (pl.col('Longitude') != 0))
    if df_loc_missing.select(pl.count()).item() > 0:
        # Add to unique location dataframe
        df_loc = df_loc.join(df_loc_missing, on='FullLocation', how='left', suffix='_n')
        df_loc = df_loc.with_columns([pl.when((pl.col('Latitude') == 0) & (pl.col('Latitude_n') != 0))
                                    .then(pl.col('Latitude_n'))
                                    .otherwise(pl.col('Latitude'))
                                    .alias('Latitude'),
                                    pl.when((pl.col('Longitude') == 0) & (pl.col('Longitude_n') != 0))
                                    .then(pl.col('Longitude_n'))
                                    .otherwise(pl.col('Longitude'))
                                    .alias('Longitude')])
        df_loc = df_loc.drop(columns=['Latitude_n', 'Longitude_n'])

        # Add to and save all known locations
        df_loc_existing = pl.concat([df_loc_existing, df_loc_missing]).unique(['FullLocation'],
                                                                              keep='first',
                                                                              maintain_order=True)
        df_loc_existing.write_parquet(cache_file)

    # Add coordinates back to main dataframe
    df = df.join(df_loc, on='FullLocation', how='left')

    return df


def date_strings_to_datetime(df, col):
    """Take a string-based date column and convert to datetime type."""
    # First handle wrongly spelled "Febuary"
    df = df.with_columns(pl.col(col).str.replace('Febuary', 'February'))
    # Convert to datetime
    col_new = f'{str(col)}Formatted'
    df = df.with_columns(pl.col(col).apply(dateparser.parse).alias(col_new))
    # If in the future then the year needs moving back one
    df = df.with_columns(pl.when(pl.col(col_new) > datetime.datetime.now())
                        .then(pl.col(col_new).dt.offset_by('-1y_saturating'))
                        .otherwise(pl.col(col_new))
                        .alias(col_new))
    return df


def run(input_paths=SCRAPED_FILES, output_path=OUTPUT_FILE,
        coordinate_path=CACHED_COORDINATE_FILE, user_agent=COORDINATE_API_USER_AGENT):
    """Load scraped sightings, add info, and save as one parquet."""
    # Import all scraped sightings
    dfs = [pl.read_parquet(f) for f in input_paths]
    df = pl.concat(dfs, how='vertical_relaxed')

    # Get full location with county and country
    df = df.with_columns(
        pl.format('{}, {}, England', 'Location', 'County').alias('FullLocation')
    )

    # Find latitude and longitude of locations
    df = add_location_coordinates_column(df, coordinate_path)

    # Format Date as a datetime
    df = date_strings_to_datetime(df, 'Date')

    # Save processed sightings
    df.write_parquet(output_path)


if __name__ == "__main__":
    run()