from configparser import ConfigParser
from pathlib import Path

current_path = Path(__file__)
secrets_cfg = current_path.parent.joinpath('secrets.cfg')

config = ConfigParser()
config.read(str(secrets_cfg))