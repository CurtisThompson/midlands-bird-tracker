import logging
import sys
from datetime import datetime
from os.path import join as path_join

from src.initialise import setup_repo
from src.extract import pull_dos, pull_lros, pull_notts
from src.transform import process_scrapes
from src.report import build_html_report

from config.config import get_config


# Import config file
CONFIG = get_config()


def run(config=CONFIG):
    # Initialise repository for pipeline run
    if config['controls']['is_setup']:
        setup_repo.run(paths=config['file_path'].values())
    
    # Set up logging
    log_name = datetime.now().strftime("%Y%m%d_%H%M%S.txt")
    log_name = path_join(config['file_path']['logging'], log_name)
    logging.basicConfig(filename=log_name,
                        level=logging.DEBUG,
                        filemode='w',
                        format='[%(asctime)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.debug(f'Logging initialised in {log_name}')
    
    # Extract data from external sources
    if config['controls']['is_extract']:
        pull_dos.run(county='Derbyshire',
                     url=config['scrape']['Derbyshire']['url'],
                     file_name=config['scrape']['Derbyshire']['file_name'],
                     file_directory=config['file_path']['scrape_path'])
        pull_lros.run(county='Leicestershire',
                     url=config['scrape']['Leicestershire']['url'],
                     file_name=config['scrape']['Leicestershire']['file_name'],
                     file_directory=config['file_path']['scrape_path'])
        pull_notts.run(county='Nottinghamshire',
                     url=config['scrape']['Nottinghamshire']['url'],
                     file_name=config['scrape']['Nottinghamshire']['file_name'],
                     file_directory=config['file_path']['scrape_path'])
    
    # Transform externally sourced data into a single clean file
    if config['controls']['is_transform']:
        input_paths = [path_join(config['file_path']['scrape_path'], f'{x["file_name"]}.parquet')
                       for x in config['scrape'].values()]
        process_scrapes.run(input_paths=input_paths,
                            output_path=config['file_path']['sightings'],
                            coordinate_path=config['file_path']['coordinates'],
                            user_agent=config['coordinate_user_agent'])
    
    # Generate html report from clean data
    if config['controls']['is_report']:
        build_html_report.run(sightings_file=config['file_path']['sightings'],
                              report_file=config['file_path']['report'],
                              n_days=config['report_previous_days'])


if __name__ == "__main__":
    run()
