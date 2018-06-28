import os
import json

import standardsearch.elasticsearchfactory

this_dir = os.path.dirname(os.path.realpath(__file__))


def load(language="english", base_url=None, extract_file=None, lang_code=None):

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
                "base_url": {"type": "keyword"},
            }
        }
    }

    elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()
    elasticsearch = elasticsearchfactory.elasticsearch
    es_index = elasticsearchfactory.index
    if lang_code:
        es_index = es_index + '_' + lang_code

    if not elasticsearch.indices.exists(es_index):
        elasticsearch.indices.create(index=es_index, body={"mappings": mappings})

    elasticsearch.delete_by_query(index=es_index,
                                  doc_type='results',
                                  body={"query": {"term": {"base_url": base_url}}})

    with open(extract_file) as f:
        results = json.load(f)

        for result in results:
            elasticsearch.index(index=es_index,
                                doc_type='results',
                                id=result['url'],
                                body=result)
