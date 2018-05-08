import os
import standardsearch.etl.scraper


def main():
    scraper = standardsearch.etl.scraper.Scraper()
    urls_file = os.path.dirname(os.path.realpath(__file__)) + '/urls.txt'
    with open(urls_file) as f:
        for line in f:
            if line.strip():
                scraper.scrape(line.strip())


if __name__ == '__main__':
    main()
