import json
import os

from elasticsearch import Elasticsearch

from standardsearch.extract_sphinx import process
from standardsearch.utils import get_http_version_of_url

LANG_MAP = {"en": "english", "fr": "french", "es": "spanish", "it": "italian"}
this_dir = os.path.dirname(os.path.realpath(__file__))


def _append_lang_code(url, language_code):
    return f"{url.rstrip('/')}/{language_code}/"


def run_scrape(version, langs, url, new_url):
    for language_code in langs:
        lang_url = _append_lang_code(url, language_code)
        if new_url:
            new_lang_url = _append_lang_code(new_url, language_code)
        else:
            new_lang_url = None

        results = process(lang_url, new_lang_url)

        load(LANG_MAP.get(language_code, "standard"), new_lang_url or lang_url, results, language_code)


def load(language, base_url, results, language_code):
    elasticsearch = Elasticsearch()
    es_index = "standardsearch_{}".format(language_code)
    doc_type = "results"

    if not elasticsearch.indices.exists(es_index):
        elasticsearch.indices.create(index=es_index, body={
            "mappings": {
                doc_type: {
                    "_all": {"analyzer": language},
                    "properties": {
                        "text": {"type": "text", "analyzer": language},
                        "title": {"type": "text", "analyzer": language},
                        "base_url": {"type": "keyword"},
                    },
                },
            },
        })

    elasticsearch.delete_by_query(
        index=es_index,
        doc_type=doc_type,
        # In our data store, we store everything with a base_url with an http address,
        # ..... so if we get a request with https, change it!
        body={"query": {"term": {"base_url": get_http_version_of_url(base_url)}}},
    )

    for result in results:
        result["base_url"] = get_http_version_of_url(result["base_url"])
        elasticsearch.index(index=es_index, doc_type=doc_type, id=result["url"], body=result)
