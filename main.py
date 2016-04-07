#!/usr/bin/env python3

from urllib.error import HTTPError
from nihg import (DATA_PATH,
                  import_grants,
                  write_rss,
                  upload_website,
                  )

grantfilters = [{'name': 'Boston',
                 'filter': lambda x: (x['ORG_CITY'] == 'BOSTON' or 'harvard' in x['ORG_NAME'].lower()),
                },
                {'name': 'Neuroscience',
                 'filter': lambda x: any([True for t in ('neur', 'brain', 'sleep') if t in x['PROJECT_TERMS']]),
                },
               ]


def main():
    try:
        grants = import_grants()

    except HTTPError:
        print('No new grants have been published')

    else:
        for filt in grantfilters:
            rss_name = DATA_PATH / 'rss' / (filt['name'].lower() + '.xml')

            with rss_name.open('w') as f:
                f.write(write_rss(grants, filt))

            upload_website(rss_name)


if __name__ == '__main__':
    main()
