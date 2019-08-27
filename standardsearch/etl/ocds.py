import tempfile
import os.path
import standardsearch.etl.extract
from standardsearch.etl.sources import Source
from standardsearch.etl.load import load

from standardsearch.etl.extract_sphinx import ExtractSphinx


LANG_MAP = {'en': 'english',
            'fr': 'french',
            'es': 'spanish',
            'it': 'italian'}


def run_scrape(version='latest', langs=('en', 'es', 'fr'), url=None, new_url=None):

    if not url:
        url = 'https://standard.open-contracting.org/{}/'.format(version)

    for lang in langs:
        lang_url = url.rstrip('/') + '/' + lang + '/'
        new_lang_url = None
        if new_url:
            new_lang_url = new_url.rstrip('/') + '/' + lang + '/'

        with tempfile.TemporaryDirectory() as tmpdirname:
            extract_file = os.path.join(tmpdirname, 'extract.json')
            extract = standardsearch.etl.extract.Extract(extract_file)
            extract.add_source(Source(url=lang_url, new_url=new_lang_url, extractor=ExtractSphinx))
            extract.go()
            load(
                base_url=(new_lang_url or lang_url),
                language=LANG_MAP.get(lang, 'standard'),
                extract_file=extract_file,
                lang_code=lang
            )
