import yaml


class Config:
    api_type = None
    access_token = None


class ArticleConfig:
    api_type = None
    access_token = None


def load_config():
    with open("D:\SCUEC-AgentChat\Agent\config\config.yaml", 'r') as file:
        config = yaml.safe_load(file)
        Config.api_type = config['api']['type']
        Config.access_token = config['api']['access_token']


def load_article_config():
    with open("D:\SCUEC-AgentChat\Agent\config\ArticleConfig.yaml", 'r') as file:
        config = yaml.safe_load(file)
        Config.api_type = config['api']['type']
        Config.access_token = config['api']['access_token']


def load_RAG_config():
    with open("D:\SCUEC-AgentChat\Agent\config\RAG.yaml", 'r') as file:
        config = yaml.safe_load(file)
        Config.access_token = config['api']['access_token']
