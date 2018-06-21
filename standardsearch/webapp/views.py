from django.http import JsonResponse
import standardsearch.elasticsearchfactory
from standardsearch.etl.ocds import run_scrape as ocds_run_scrape
from django.conf import settings


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

def index_ocds(request):
    secret = request.GET.get('secret')
    version = request.GET.get('version')
    index_version = request.GET.get('index_version')

    error = None
    new_url = None

    if not secret:
         error = "Need to supply a secret"
    elif not version:
         error = "Need to supply a version"
    elif secret != settings.OCDS_SECRET:
         error = "secret not correct"


    if not error:
        url = 'http://standard.open-contracting.org/{}/'.format(version)
        if index_version:
            new_url = 'http://standard.open-contracting.org/{}/'.format(index_version)
        try:
            ocds_run_scrape(version=version, url=url, new_url=new_url)
        except Exception as e:
            error = str(e)

    if error:
        resp = JsonResponse({"error": error})
    else:
        resp = JsonResponse({"sucess": True})

    resp['Access-Control-Allow-Origin'] = '*'
    return resp
