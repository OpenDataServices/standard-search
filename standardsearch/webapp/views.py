from django.http import JsonResponse
import standardsearch.elasticsearchfactory


def search_v1(request):
    search = request.GET.get('q', '')
    base_url = request.GET.get('base_url', '')

    elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()

    query = {
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": search, 
                        "fields" : ["text", "title^3"], "default_operator": "and"
                    },
                },
                "filter": {"term": {"base_url": base_url}},
            }
        }, 
        "highlight": {"fields": {"text": {}, "title": {}}}
    }

    res = elasticsearchfactory.get().search(index=elasticsearchfactory.index,
                                            body=query, size=100)

    out = {
        'results': [],
        'count': res['hits']['total'],
           }

    for hit in res['hits']['hits']:
        out['results'].append({
            "title": hit['_source']['title'],
            "url": hit['_source']['url'],
            "highlights": hit['highlight'].get('text', hit['highlight'].get('title')),
        })


    resp = JsonResponse(out)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
