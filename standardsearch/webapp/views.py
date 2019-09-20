from django.http import JsonResponse
import standardsearch.elasticsearchfactory
from standardsearch.etl.ocds import run_scrape as ocds_run_scrape
from django.conf import settings
from standardsearch.utils import get_http_version_of_url


def search_v1(request):
    search = request.GET.get('q', '')
    base_url = request.GET.get('base_url', '')

    # We use base_url to decide which set of documents to search,
    # .... but that can be on http or https, it should be the same documents on both!
    # In our data store, we store everything with a base_url with an http address,
    # ..... so if we get a request with https, change it!
    base_url = get_http_version_of_url(base_url)

    lang = None
    split = base_url.rstrip("/").split('/')
    if split:
        lang = split[-1]

    elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()
    es_index = elasticsearchfactory.index
    if lang:
        es_index = es_index + '_' + lang

    query = {
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": search,
                        "fields": ["text", "title^3"], "default_operator": "and"
                    },
                },
                "filter": {"term": {"base_url": base_url}},
            }
        },
        "highlight": {"fields": {"text": {}, "title": {}}}
    }

    res = elasticsearchfactory.get().search(index=es_index,
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
    # These were the default languages at the point this parameter was introduced, so keep them as the default
    langs_raw = request.GET.get('langs', 'en,es,fr')
    langs = [lang.strip() for lang in langs_raw.split(',')]

    error = None
    new_url = None

    if not secret:
        error = "Need to supply a secret"
    elif not version:
        error = "Need to supply a version"
    elif secret != settings.OCDS_SECRET:
        error = "secret not correct"

    if not error:
        url = 'https://standard.open-contracting.org/{}/'.format(version)
        if index_version:
            new_url = 'https://standard.open-contracting.org/{}/'.format(index_version)
        try:
            ocds_run_scrape(version=version, url=url, new_url=new_url, langs=langs)
        except Exception as e:
            error = str(e)

    if error:
        resp = JsonResponse({"error": error})
    else:
        resp = JsonResponse({"success": True})

    resp['Access-Control-Allow-Origin'] = '*'
    return resp
