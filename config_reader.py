import json


class ConfigReader:

    urls = []

    def __init__(self, path):
        configfile = open(path, 'r')
        self.config = json.loads(configfile.read())

    def get_urls(self):
        return self.config['sites']

    def get_db_details(self):
        return self.config['database']

