from twython import Twython
from .credentials import config

APP_KEY = config['twitter']['app_key']
APP_SECRET = config['twitter']['app_secret']

oauth_token = config['twitter']['oauth_token']
oauth_token_secret = config['twitter']['oauth_token_secret']

URL_DETAILS = 'https://projectreporter.nih.gov/project_info_details.cfm?aid='

twitter = Twython(APP_KEY, APP_SECRET, oauth_token, oauth_token_secret)

MAX_TITLE_LEN = 98


def write_tweet(grant):
    FUNDING_ICs = grant['FUNDING_ICs'].split(':')[0]
    TITLE = grant['PROJECT_TITLE']
    if len(TITLE) > MAX_TITLE_LEN:
        TITLE = TITLE[:MAX_TITLE_LEN - 3] + '...'

    t = '#{} funds #{}: {} {}{}'.format(FUNDING_ICs,
                                        grant['ACTIVITY'],
                                        TITLE,
                                        URL_DETAILS,
                                        grant['APPLICATION_ID'],
                                        )

    return t
