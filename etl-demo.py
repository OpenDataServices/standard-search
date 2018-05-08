import standardsearch.etl.process
from standardsearch.etl.sources import Source


def main():
    process = standardsearch.etl.process.Process()

    process.add_source(Source(url='http://example.com/'))

    process.add_source(Source(url='http://opendataservices.coop/'))

    process.go()


if __name__ == '__main__':
    main()
