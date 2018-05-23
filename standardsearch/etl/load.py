import os
import json
import copy

from elasticsearch import Elasticsearch
import standardsearch.elasticsearchfactory


this_dir = os.path.dirname(os.path.realpath(__file__))


def load(es_index='standardsearch', language="english", extract_file=None):

    if not extract_file:
        extract_file = os.path.join(this_dir, '../../extracted_data.json')

    mappings = {
        "results": {
            "_all": {
                "analyzer": language
            },
            "properties": {
                "text": {"type": "text", "analyzer": language},
                "title": {"type": "text", "analyzer": language},
            }
        }
    }

    elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory(es_index)
    elasticsearch = elasticsearchfactory.elasticsearch

    elasticsearch.indices.delete(index=es_index, ignore=[400, 404])
    elasticsearch.indices.create(index=es_index, body={"mappings": mappings})
    with open(extract_file) as f:
        results = json.load(f)

        for result in results:
            elasticsearch.index(index=es_index,
                                doc_type='results',
                                id=result['url'],
                                body=result)

