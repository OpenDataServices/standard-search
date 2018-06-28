import standardsearch.etl.extractbs4 as extractbs4


class Source:
    def __init__(self, url=None, new_url=None, extractor=extractbs4.ExtractBS4):
        self.url = url
        self.new_url = new_url
        self.extractor = extractor()

    def extract(self):
        return self.extractor.process(self)
