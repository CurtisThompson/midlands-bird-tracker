import polars as pl
from datetime import datetime, timedelta

df = pl.read_parquet('./data/bird_sightings.parquet')

# Filter last five days
df = df.filter(pl.col('DateFormatted').is_between(datetime.now() - timedelta(days=5), datetime.now()))

# Sort by diaply order
df = df.sort(by=pl.col('County'), descending=False).sort(by=pl.col('DateFormatted'), descending=True)

# Display
current_date = None
current_county = None
date_changed = True
for row in df.rows(named=True):
    # If new date, display
    if row['DateFormatted'] != current_date:
        print()
        print()
        print(row['DateFormatted'].strftime('%A %d %m %Y'))
        current_date = row['DateFormatted']
        date_changed = True
    
    # If new county, display
    if (row['County'] != current_county) or (date_changed):
        print(row['County'])
        current_county = row['County']
    
    print(row['Location'])
    print(row['BirdText'])
    print()

    date_changed = False


# Display as...
# Date
# County: Location
# sightings, sightings, sightings
# County: Location
# sightings, sightings, sightings
#
# Date
# ...