from elasticsearch import Elasticsearch

"""Creates a ElasticSearch object for other code to use.

This is a separate class because at some stage we'll need to remove the hard coded URL (it assumes localhost:9200), 
index and doctype and make those configurable. So having only one place that creates the objects helps.

(I think Factory is the wrong pattern term here - technically this returns a singleton object. But not sure if that 
matters, or what right term is!)"""
class ElasticSearchFactory:
    elasticsearch = None
    index = 'standardsearch'
    doctype = 'result'

    def __init__(self):
        self.elasticsearch = Elasticsearch()

    def get(self):
        return self.elasticsearch
