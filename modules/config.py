import yaml

def load_marketplaces():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config.get('marketplaces', [])
