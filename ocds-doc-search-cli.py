import standardsearch.etl.extract
from standardsearch.etl.sources import Source
from standardsearch.etl.load import load

from standardsearch.etl.extract_sphinx import ExtractSphinx

import argparse

LANG_MAP = {'en': 'english',
            'fr': 'french',
            'es': 'spanish'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to learn basic argparse')
    parser.add_argument('-v', '--version',
                        help='OCDS Version',
                        required='True')
    parser.add_argument('-l', '--lang',
                        help='Two letter language code',
                        required='True')
    parser.add_argument('-u', '--url',
                        help='Doc url endpoint to scrape docs',
                        default='')

    args = parser.parse_args()

    es_index = 'ocds-doc-search-{}-{}'.format(args.version, args.lang)

    url = args.url
    if not args.url:
        url = 'http://standard.open-contracting.org/{}/{}/'.format(args.version, args.lang)

    extract = standardsearch.etl.extract.Extract()
    extract.add_source(Source(url=url, extractor=ExtractSphinx))
    extract.go()
    load(es_index=es_index, language=LANG_MAP.get(args.lang, 'standard'))


