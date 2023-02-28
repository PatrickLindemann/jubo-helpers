import json
from src.model.config import Config, Server, User

def read_config(config_path: str) -> Config:
    """Read the config from a JSON file.

    Parameters
    ----------
    config_path : str
        The path to the configuration file

    Returns
    -------
    Config
        The parsed config
    """
    with open(config_path) as file:
        data = json.load(file)
    # Convert the json data to a Config dataclass object and return it
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