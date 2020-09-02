class Source:
    def __init__(self, url=None, new_url=None, extractor=None):
        self.url = url
        self.new_url = new_url
        self.extractor = extractor()

    def extract(self):
        return self.extractor.process(self)
