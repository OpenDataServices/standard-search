import standardsearch.etl.extract
from standardsearch.etl.sources import Source
from standardsearch.etl.load import load

from standardsearch.etl.extract_sphinx import ExtractSphinx

import argparse

LANG_MAP = {'en': 'english',
            'fr': 'french',
            'es': 'spanish'}


def run_scrape(version, langs=('en', 'es', 'fr'), url=None):

    if not url:
        url = 'http://standard.open-contracting.org/{}/'.format(version)

    for lang in langs:
        lang_url = url.rstrip('/') + '/' + lang + '/'
        extract = standardsearch.etl.extract.Extract()
        extract.add_source(Source(url=lang_url, extractor=ExtractSphinx))
        extract.go()
        load(base_url=lang_url, language=LANG_MAP.get(lang, 'standard'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to learn basic argparse')
    parser.add_argument('-v', '--version',
                        default='',
                        help='OCDS Version')
    parser.add_argument('-l', '--langs',
                        help='Two letter languages codes seperated by a comma ,',
                        default='en,fr,es')
    parser.add_argument('-u', '--url',
                        help='Doc url enpoint(without language part) to scrape docs',
                        default='')

    args = parser.parse_args()

    langs = [lang.strip() for lang in  args.langs.split(',')]

    run_scrape(args.version or 'latest', langs, args.url)



