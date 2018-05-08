import requests
from bs4 import BeautifulSoup


class ProcessBS4:
    elasticsearchfactory = None

    def __init__(self, elasticsearchfactory=elasticsearchfactory):
        self.elasticsearchfactory = elasticsearchfactory

    def process(self, source):
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
