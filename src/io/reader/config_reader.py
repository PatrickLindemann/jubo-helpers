import json

from src.model.config import Config, Server, User

def read_config(file_path):
    with open(file_path) as file:
        data = json.load(file)
    user = User(data['user']['email'], data['user']['password'])
    servers = {
        'imap': Server(
            data['servers']['imap']['host'],
            data['servers']['imap']['port']
        ),
        'smtp': Server(
            data['servers']['smtp']['host'],
            data['servers']['smtp']['port']
        )
    }
    return Config(user, servers)