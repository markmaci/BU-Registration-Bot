import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

USERNAME = config['username']
PASSWORD = config['password']