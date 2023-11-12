import os


FILE_PATHS = []


def run(paths=FILE_PATHS):
    # Get unique list of directories
    dir_names = [os.path.dirname(p) for p in paths]
    dir_names = list(set(dir_names))
    
    # Create all directories if they don't exist
    for d in dir_names:
        os.makedirs(d, exist_ok=True)


if __name__ == "__main__":
    run()