import os
import json

from elasticsearch import Elasticsearch

ES_INDEX = os.environ.get('ES_INDEX', 'standardsearch') 

elasticsearch = Elasticsearch()

this_dir = os.path.dirname(os.path.realpath(__file__))

def load():
    elasticsearch.indices.delete(index=ES_INDEX, ignore=[400, 404])
    elasticsearch.indices.create(index=ES_INDEX)
    with open(os.path.join(this_dir, '../../extracted_data.json')) as f:
        results = json.load(f)

        for result in results:
            elasticsearch.index(index=ES_INDEX,
                                doc_type='results',
                                id=result['url'],
                                body=result)

