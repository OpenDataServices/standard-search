import standardsearch.etl.extract
from standardsearch.etl.sources import Source
from standardsearch.etl.load import load

from standardsearch.etl.extract_sphinx import ExtractSphinx


def main():
    extract = standardsearch.etl.extract.Extract()

    extract.add_source(Source(url='http://example.com/'))
    extract.add_source(Source(url='http://opendataservices.coop/'))

    extract.add_source(Source(url='http://standard.open-contracting.org/latest/en/', extractor=ExtractSphinx))

    extract.go()

    load()


if __name__ == '__main__':
    main()
