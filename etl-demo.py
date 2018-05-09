import standardsearch.etl.extract
from standardsearch.etl.sources import Source
from standardsearch.etl.load import load


def main():
    extract = standardsearch.etl.extract.Extract()

    extract.add_source(Source(url='http://example.com/'))

    extract.add_source(Source(url='http://opendataservices.coop/'))

    extract.go()

    load()


if __name__ == '__main__':
    main()
