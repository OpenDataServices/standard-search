import os
import json

from elasticsearch import Elasticsearch
import standardsearch.elasticsearchfactory

elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()
elasticsearch = elasticsearchfactory.elasticsearch
es_index = elasticsearchfactory.index

this_dir = os.path.dirname(os.path.realpath(__file__))

def load():
    elasticsearch.indices.delete(index=es_index, ignore=[400, 404])
    elasticsearch.indices.create(index=es_index)
    with open(os.path.join(this_dir, '../../extracted_data.json')) as f:
        results = json.load(f)

        for result in results:
            elasticsearch.index(index=es_index,
                                doc_type='results',
                                id=result['url'],
                                body=result)

