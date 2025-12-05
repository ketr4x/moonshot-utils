import json

def read_config(param):
    with open('config.json') as config_file:
        config = json.load(config_file)
    if param in config:
        return config[param]
    else:
        return None