import os


def initialise_repository():
    os.makedirs('./data/scrape_extracts/', exist_ok=True)
    os.makedirs('./reports/', exist_ok=True)


if __name__ == "__main__":
    initialise_repository()