import polars as pl
from geopy.geocoders import Nominatim
from time import sleep
from random import random
import dateutil.parser as dateparser
import datetime


def get_location_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="midlands-bird-tracker")
        loc = geolocator.geocode(location)
        sleep(random())
        return {'Latitude':loc.latitude, 'Longitude':loc.longitude}
    except:
        return {'Latitude':0.0, 'Longitude':0.0}


# Import all scraped sightings
dfs = [pl.read_parquet('./data/scrape_extracts/dos.parquet'),
       pl.read_parquet('./data/scrape_extracts/lros.parquet'),
       pl.read_parquet('./data/scrape_extracts/notts.parquet')]
df = pl.concat(dfs, how='vertical_relaxed')

# Get full location with county and country
df = df.with_columns(
    pl.format('{}, {}, England', 'Location', 'County').alias('FullLocation')
)

# Get dataframe of unique locations
df_loc = df.unique('FullLocation').select('FullLocation')

# Load existing locations
df_loc_existing = df._read_parquet('./data/location_coordinates.parquet')

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
    df_loc_existing = pl.concat([df_loc_existing, df_loc_missing]).unique(['FullLocation'], keep='first', maintain_order=True)
    df_loc_existing.write_parquet('./data/location_coordinates.parquet')

# Add coordinates back to main dataframe
df = df.join(df_loc, on='FullLocation', how='left')

# Format Date as a datetime
df = df.with_columns(pl.col('Date').apply(dateparser.parse).alias('DateFormatted'))
# If in the future then the year needs moving back one
df = df.with_columns(pl.when(pl.col('DateFormatted') > datetime.datetime.now())
                     .then(pl.col('DateFormatted').dt.offset_by('-1y'))
                     .otherwise(pl.col('DateFormatted'))
                     .alias('DateFormatted'))