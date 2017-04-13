from pathlib import Path

DATA_PATH = Path('/home/gio/projects/nihg/data')

from .importer import import_grants
from .twitter import write_tweet
from .rss import write_rss
from .ftp import upload_website
