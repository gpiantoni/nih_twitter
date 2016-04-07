from datetime import date, datetime
from html import escape


HEADER = ('<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel>\n'
          '<title>{granttype}</title>\n'
          '<link>http://projectreporter.nih.gov/</link>\n'
          '<description>RSS feeds of NIH grants</description>\n'
          '<lastBuildDate>{date:%d %b %Y}</lastBuildDate>\n'
          '<language>en-us</language>\n')

ITEM = ('<item>\n'
        '\t<title>{activity} {title}</title>\n'
        '\t<description>{description}</description>\n'
        '\t<link>http://projectreporter.nih.gov/project_info_description.cfm?aid={ID}</link>\n'
        '</item>\n')

DESCR = ('to: {pi}<br />'
         'at {dept}{org}, {city}, {state}<br/><br/>'
         'Year: {year:<2}<br/>'
         '{startdate} - {enddate}<br />'
         'Costs:{costs: 10,d} USD<br /><br/>'
         '{abstract}')

FOOTER = ('</channel>\n'
          '</rss>\n')


def write_rss(grants, granttype):

    grant = filter(lambda x: not x['ACTIVITY'][0] in ('P', 'U', 'I'), grants)

    # list because we run loop twice
    grants = list(filter(granttype['filter'], grants))

    # otherwise it cannot sort the grants
    for grant in grants:
        if grant['SUPPORT_YEAR'] == '':
            grant['SUPPORT_YEAR'] = 0

        if grant['TOTAL_COST'] == '':
            grant['TOTAL_COST'] = 0
        else:
            grant['TOTAL_COST'] == int(grant['TOTAL_COST'])

    grants = sorted(grants, key=lambda x: (x['ACTIVITY'],
                                           int(x['SUPPORT_YEAR']),
                                           x['TOTAL_COST']))
    header = HEADER.format(granttype=granttype['name'],
                           date=date.today())

    g = []
    for grant in grants:

        authors = grant['PI_NAMEs'].title().strip(' ;')
        pi = '; '.join(_fix_author_name(a) for a in authors.split(';'))

        try:
            start = ('{:%b %Y}'
                     ''.format(datetime.strptime(grant['PROJECT_START'],
                                                 '%m/%d/%Y')))
            end = ('{:%b %Y}'
                   ''.format(datetime.strptime(grant['PROJECT_END'],
                                               '%m/%d/%Y')))
        except ValueError:
            start = grant['PROJECT_START']
            end = grant['PROJECT_END']

        if grant['ORG_DEPT'] == '':
            dept = ''
        else:
            dept = 'Dept. {}, '.format(grant['ORG_DEPT'].title())

        descr = DESCR.format(pi=pi,
                             dept=dept,
                             org=grant['ORG_NAME'].title(),
                             city=grant['ORG_CITY'].title(),
                             state=grant['ORG_STATE'],
                             abstract=grant['abstract'],
                             costs=grant['TOTAL_COST'],
                             year=grant['SUPPORT_YEAR'],
                             startdate=start,
                             enddate=end)

        g.append(ITEM.format(activity=grant['ACTIVITY'],
                             title=escape(grant['PROJECT_TITLE']),
                             description=escape(descr),
                             ID=grant['APPLICATION_ID']))

    return header + '\n'.join(g) + FOOTER


def _fix_author_name(author):
    author = author.replace(' (Contact)', '')
    return ' '.join(author.split(', ')[::-1])
