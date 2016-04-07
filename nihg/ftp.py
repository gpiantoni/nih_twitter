from ftplib import FTP
from .credentials import config

ftp_user = config['ftp']['user']
ftp_passwd = config['ftp']['passwd']


def upload_website(grants_file):

    with FTP("ftp.gpiantoni.com") as ftp:
        ftp.login(ftp_user, ftp_passwd)

        with grants_file.open('rb') as f:
            ftp.storlines('STOR ' + grants_file.name, f)
