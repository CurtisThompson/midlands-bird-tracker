from src.initialise import setup_repo
from src.extract import pull_dos, pull_lros, pull_notts
from src.transform import process_scrapes
from src.report import build_html_report


SAMPLE_CONFIG = {
    'is_setup' : False,
    'is_extract' : True,
    'is_transform' : False,
    'is_report' : False
}


def run(config=SAMPLE_CONFIG):
    if config['is_setup']:
        setup_repo.run()
    
    if config['is_extract']:
        pull_dos.run()
        pull_lros.run()
        pull_notts.run()
    
    if config['is_transform']:
        process_scrapes.run()
    
    if config['is_report']:
        build_html_report.run()


if __name__ == "__main__":
    run()
