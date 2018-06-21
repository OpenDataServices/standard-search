import argparse
from standardsearch.etl.ocds import run_scrape


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
    parser.add_argument('-n', '--newurl',
                        help='Endpoint as it will appear is search index',
                        default='')

    args = parser.parse_args()

    langs = [lang.strip() for lang in  args.langs.split(',')]

    run_scrape(args.version or 'latest', langs, args.url, new_url=args.newurl)



