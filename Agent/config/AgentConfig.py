import yaml


class Config:
    api_type = None
    access_token = None


def load_config():
    with open('D:/Agent/config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        Config.api_type = config['api']['type']
        Config.access_token = config['api']['access_token']
