import os
import polars as pl
from datetime import datetime, timedelta
from premailer import Premailer


PREVIOUS_N_DAYS = 5
SIGHTINGS_FILE = './data/bird_sightings.parquet'
REPORT_FILE = './reports/recent-report.html'
CSS_FILE = './reports/style.css'

HTML_HEADER = '''<html>
<head>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="report-container">
<h1>Recent Midlands Bird Sightings</h1>\n'''
HTML_FOOTER = '</div>\n</body>\n</html>'


def prepare_dataframe(df, n_days=PREVIOUS_N_DAYS):
    """Filter and sort dataframe ready for reporting."""
    # Filter last five days
    df = df.filter(pl.col('DateFormatted').is_between(datetime.now() - timedelta(days=n_days), datetime.now()))

    # Sort by display order
    df = df.sort(by=pl.col('County'), descending=False).sort(by=pl.col('DateFormatted'), descending=True)

    return df


def build_html_string(df, header=HTML_HEADER, footer=HTML_FOOTER):
    """Build a HTML report from a sightings dataframe."""
    html = header

    # Display
    current_date = None
    current_county = None
    for row in df.rows(named=True):
        # If new date, display
        if row['DateFormatted'] != current_date:
            if current_date != None:
                html += '</div>\n</div>\n'
            html += f'<div class="date-container">\n<h2 class="date-header">{row["DateFormatted"].strftime("%A %d %B %Y")}</h2>\n'
            current_date = row['DateFormatted']
            current_county = None
        
        # If new county, display
        if (row['County'] != current_county):
            if current_county != None:
                html += '</div>'
            html += f'<div class="county-container">\n<h3 class="county-header">{row["County"]}</h3>\n'
            current_county = row['County']
        
        # Add sighting info
        html += f'<h4 class="location-header">{row["Location"]}</h4>\n'
        html += f'<p class="bird-sighting">{row["BirdText"]}</p>\n'

    # Add footer
    html += '</div>\n</div>\n'
    html += footer

    return html


def inline_stylise(html, css):
    """Move external styling into inline-styling for html string."""
    css_dir = os.path.dirname(css)
    css_file = os.path.basename(css)
    premail_styler = Premailer(external_styles=css_file,
                               base_path=css_dir,
                               allow_loading_external_files=True)
    html_transformed = premail_styler.transform(html)
    return html_transformed


def run(sightings_file=SIGHTINGS_FILE, report_file=REPORT_FILE,
        css_file=CSS_FILE, n_days=PREVIOUS_N_DAYS):
    """Load sightings parquet and build HTML report."""
    df = pl.read_parquet(sightings_file)
    df = prepare_dataframe(df, n_days=n_days)

    html = build_html_string(df)

    html = inline_stylise(html, css_file)

    with open(report_file, 'w+') as f:
        f.write(html)


if __name__ == "__main__":
    run()