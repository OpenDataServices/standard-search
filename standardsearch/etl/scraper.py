import requests
from bs4 import BeautifulSoup
import standardsearch.elasticsearchfactory


class Scraper:
    elasticsearchfactory = None

    def __init__(self):
        self.elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()

    def scrape(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            body = {
                'url': url,
                'text': soup.get_text(),
                'title': soup.title.string,
            }
            self.elasticsearchfactory.get().index(index=self.elasticsearchfactory.index,
                                                  doc_type=self.elasticsearchfactory.doctype,
                                                  id=url,
                                                  body=body
                                                  )
