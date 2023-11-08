import polars as pl
from datetime import datetime, timedelta

df = pl.read_parquet('./data/bird_sightings.parquet')

# Filter last five days
df = df.filter(pl.col('DateFormatted').is_between(datetime.now() - timedelta(days=5), datetime.now()))

# Sort by display order
df = df.sort(by=pl.col('County'), descending=False).sort(by=pl.col('DateFormatted'), descending=True)

# Display
current_date = None
current_county = None
date_changed = True
html = ''
for row in df.rows(named=True):
    # If new date, display
    if row['DateFormatted'] != current_date:
        html += f'<h2 class="date-header">{row["DateFormatted"].strftime("%A %d %m %Y")}</h2>\n'
        current_date = row['DateFormatted']
        date_changed = True
    
    # If new county, display
    if (row['County'] != current_county) or (date_changed):
        html += f'<h3 class="county-header">{row["County"]}</h3>\n'
        current_county = row['County']
    
    html += f'<h4 class="location-header">{row["Location"]}</h4>\n'
    html += f'<p class="bird-sighting">{row["BirdText"]}</p>\n'

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

with open('./reports/recent-report.html', 'w+') as f:
    f.write(html)