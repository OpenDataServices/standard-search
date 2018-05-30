from django.http import JsonResponse
import standardsearch.elasticsearchfactory


def search_v1(request):
    search = request.GET.get('q', '')
    index = request.GET.get('index', 'standardsearch')

    elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory(index)

    query = {"query": {"query_string": {"query": search, "fields" : ["text", "title^3"], "default_operator": "and"}}, "highlight": {"fields": {"text": {}, "title": {}}}}

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
