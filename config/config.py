from yaml import load, Loader

def get_config():
    with open('./config/config.yaml') as f:
        return load(f, Loader=Loader)