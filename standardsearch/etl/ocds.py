import json
import os
import tempfile

from standardsearch.etl.extract_sphinx import ExtractSphinx
from standardsearch.etl.load import load

LANG_MAP = {"en": "english", "fr": "french", "es": "spanish", "it": "italian"}
this_dir = os.path.dirname(os.path.realpath(__file__))


class Extract:
    """
    Main Process class, that calls specific process classes to do actual work.

    The reason for this is that it's not clear at this stage which method will field the best results (bs4, lxml, etc).
    It may even turn out that different methods will be better for different pages. In this way, we can work on several
    alternative methods at once.
    """
    def __init__(self, extract_file=None):
        self.sources = []
        if not extract_file:
            extract_file = os.path.join(this_dir, "../../extracted_data.json")
        self.extract_file = extract_file

    def add_source(self, source):
        self.sources.append(source)

    def go(self):
        output = []
        for source in self.sources:
            output.extend(source.extract())

        with open(self.extract_file, "w+") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)


class Source:
    def __init__(self, url=None, new_url=None, extractor=None):
        self.url = url
        self.new_url = new_url
        self.extractor = extractor()

    def extract(self):
        return self.extractor.process(self)


def run_scrape(version="latest", langs=("en", "es", "fr"), url=None, new_url=None):

    if not url:
        url = "https://standard.open-contracting.org/{}/".format(version)

    for lang in langs:
        lang_url = url.rstrip("/") + "/" + lang + "/"
        new_lang_url = None
        if new_url:
            new_lang_url = new_url.rstrip("/") + "/" + lang + "/"

        with tempfile.TemporaryDirectory() as tmpdirname:
            extract_file = os.path.join(tmpdirname, "extract.json")
            extract = Extract(extract_file)
            extract.add_source(
                Source(url=lang_url, new_url=new_lang_url, extractor=ExtractSphinx)
            )
            extract.go()
            load(
                base_url=(new_lang_url or lang_url),
                language=LANG_MAP.get(lang, "standard"),
                extract_file=extract_file,
                lang_code=lang,
            )
