import requests
from bs4 import BeautifulSoup
import standardsearch.elasticsearchfactory


class Process:
    elasticsearchfactory = None
    sources = []

    def __init__(self):
        self.elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()

    def add_source(self, source):
        self.sources.append(source)

    def go(self):
        for source in self.sources:
            r = requests.get(source.url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')

                body = {
                    'url': source.url,
                    'text': soup.get_text(),
                    'title': soup.title.string,
                }
                self.elasticsearchfactory.get().index(index=self.elasticsearchfactory.index,
                                                      doc_type=self.elasticsearchfactory.doctype,
                                                      id=source.url,
                                                      body=body
                                                      )
