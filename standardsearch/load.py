import json
import os

from elasticsearch import Elasticsearch

from standardsearch.utils import get_http_version_of_url

this_dir = os.path.dirname(os.path.realpath(__file__))


def load(language="english", base_url=None, extract_file=None, lang_code=None):

    # In our data store, we store everything with a base_url with an http address,
    # ..... so if we get a request with https, change it!
    base_url = get_http_version_of_url(base_url)

    if not extract_file:
        extract_file = os.path.join(this_dir, "../../extracted_data.json")

    mappings = {
        "results": {
            "_all": {"analyzer": language},
            "properties": {
                "text": {"type": "text", "analyzer": language},
                "title": {"type": "text", "analyzer": language},
                "base_url": {"type": "keyword"},
            },
        }
    }

    elasticsearch = Elasticsearch()
    es_index = 'standardsearch'
    if lang_code:
        es_index = es_index + "_" + lang_code

    if not elasticsearch.indices.exists(es_index):
        elasticsearch.indices.create(index=es_index, body={"mappings": mappings})

    elasticsearch.delete_by_query(
        index=es_index,
        doc_type="results",
        body={"query": {"term": {"base_url": base_url}}},
    )

    with open(extract_file) as f:
        results = json.load(f)

        for result in results:
            result["base_url"] = get_http_version_of_url(result["base_url"])
            elasticsearch.index(
                index=es_index, doc_type="results", id=result["url"], body=result
            )
