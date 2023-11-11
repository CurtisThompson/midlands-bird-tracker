from src.initialise import setup_repo
from src.extract import pull_dos, pull_lros, pull_notts
from src.transform import process_scrapes
from src.report import build_html_report

from config.config import get_config


CONFIG = get_config()


def run(config=CONFIG):
    if config['controls']['is_setup']:
        setup_repo.run()
    
    if config['controls']['is_extract']:
        pull_dos.run()
        pull_lros.run()
        pull_notts.run()
    
    if config['controls']['is_transform']:
        process_scrapes.run(input_paths=config['file_path']['scrape_path'],
                            output_path=config['file_path']['sightings'],
                            coordinate_path=config['file_path']['coordinates'],
                            user_agent=config['coordinate_user_agent'])
    
    if config['controls']['is_report']:
        build_html_report.run(sightings_file=config['file_path']['sightings'],
                              report_file=config['file_path']['report'],
                              n_days=config['report_previous_days'])


if __name__ == "__main__":
    run()
