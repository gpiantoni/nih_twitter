import csv
from urllib.request import urlretrieve
from pathlib import Path
from zipfile import ZipFile

from . import DATA_PATH


URL_REPORTER = 'http://exporter.nih.gov/CSVs/final/'
CSV_PATH = DATA_PATH / 'csv'
NIH_NAME = 'RePORTER_{type}_C_FY{fy}_{week:03d}'


def import_grants():
    fy, week = _find_latest_fy_week()
    return _read_grants(fy, week + 1)


def _read_grants(fy, week):

    output = []
    for prj in ('PRJ', 'PRJABS'):
        nih_name = Path(NIH_NAME.format(type=prj, fy=fy, week=week))
        csv_file = CSV_PATH / nih_name.with_suffix('.csv')
        if not csv_file.exists():
            download_reporter(prj, fy, week)

        output.append(read_csv(csv_file))

    grants = _merge_abstracts(*output)

    return grants


def download_reporter(prj, fy, week):

    nih_name = Path(NIH_NAME.format(type=prj, fy=fy, week=week))
    url = URL_REPORTER + nih_name.with_suffix('.zip').name
    zip_file = CSV_PATH / nih_name.with_suffix('.zip')
    urlretrieve(url, str(zip_file))
    print('Reading ' + str(url))

    with ZipFile(str(zip_file)) as z:
        z.extract(str(nih_name.with_suffix('.csv')), path=str(CSV_PATH))

    zip_file.unlink()


def read_csv(csv_file):
    grants = []

    with csv_file.open(newline='', encoding='latin_1') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            grants.append(row)

    return grants


def _merge_abstracts(grants, abstracts):

    for grant in grants:
        grant['abstract'] = _find_abstract(grant, abstracts)

    return grants


def _find_abstract(grant, abstracts):
    for abstract in abstracts:
        if abstract['APPLICATION_ID'] == grant['APPLICATION_ID']:
            abs_t = abstract['ABSTRACT_TEXT']

            if abs_t == '':
                return '(empty abstract)'

            abs_t = abs_t.replace('DESCRIPTION (provided by applicant):', '')
            abs_t = abs_t.replace('DESCRIPTION:', '')
            abs_t = abs_t.replace('PROJECT SUMMARY', '')
            abs_t = abs_t.replace('(See instructions):', '')
            abs_t = abs_t.replace('(See Instructions):', '')

            if abs_t == '':
                return '(empty abstract)'

            if abs_t[0] == '?':
                abs_t = abs_t[1:]
            abs_t = abs_t.strip()
            return abs_t

    else:
        return '(not available)'


def _find_latest_fy_week():
    max_year = max_week = 0
    for one_csv in CSV_PATH.glob('RePORTER_PRJ_*.csv'):
        try:
            year = int(one_csv.stem.split('_')[3][2:])
            week = int(one_csv.stem.split('_')[4])
        except Exception:
            continue

        if year >= max_year and week >= max_week:
            max_year = year
            max_week = week

    return max_year, max_week
