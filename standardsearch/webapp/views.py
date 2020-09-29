from elasticsearch import Elasticsearch
from django.conf import settings
from django.http import JsonResponse

from standardsearch.extract_sphinx import process

LANG_MAP = {"en": "english", "fr": "french", "es": "spanish", "it": "italian"}


def _append_lang_code(url, language_code):
    return f"{url.rstrip('/')}/{language_code}/"


def _get_http_version_of_url(url):
    if url.startswith("https://"):
        return "http" + url[5:]
    else:
        return url


def _load(language, base_url, results, language_code):
    elasticsearch = Elasticsearch()
    es_index = "standardsearch_{}".format(language_code)
    doc_type = "results"

    if not elasticsearch.indices.exists(es_index):
        elasticsearch.indices.create(index=es_index, body={
            "mappings": {
                doc_type: {
                    "_all": {"analyzer": language},
                    "properties": {
                        "text": {"type": "text", "analyzer": language},
                        "title": {"type": "text", "analyzer": language},
                        "base_url": {"type": "keyword"},
                    },
                },
            },
        })

    elasticsearch.delete_by_query(
        index=es_index,
        doc_type=doc_type,
        # In our data store, we store everything with a base_url with an http address,
        # ..... so if we get a request with https, change it!
        body={"query": {"term": {"base_url": _get_http_version_of_url(base_url)}}},
    )

    for result in results:
        result["base_url"] = _get_http_version_of_url(result["base_url"])
        elasticsearch.index(index=es_index, doc_type=doc_type, id=result["url"], body=result)


def _respond(content):
    resp = JsonResponse(content)
    resp["Access-Control-Allow-Origin"] = "*"
    return resp


def search_v1(request):
    q = request.GET.get("q", "")
    base_url = request.GET.get("base_url", "")

    # We use base_url to decide which set of documents to search,
    # .... but that can be on http or https, it should be the same documents on both!
    # In our data store, we store everything with a base_url with an http address,
    # ..... so if we get a request with https, change it!
    base_url = _get_http_version_of_url(base_url)

    split = base_url.rstrip("/").split("/")
    if split:
        lang = split[-1]
    else:
        lang = None

    es_index = "standardsearch"
    if lang:
        es_index = es_index + "_" + lang

    res = Elasticsearch().search(index=es_index, size=100, body={
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": q,
                        "fields": ["text", "title^3"],
                        "default_operator": "and",
                    },
                },
                "filter": {"term": {"base_url": base_url}},
            }
        },
        "highlight": {"fields": {"text": {}, "title": {}}},
    })

    content = {
        "results": [],
        "count": res["hits"]["total"],
    }

    for hit in res["hits"]["hits"]:
        content["results"].append(
            {
                "title": hit["_source"]["title"],
                "url": hit["_source"]["url"],
                "highlights": hit["highlight"].get(
                    "text", hit["highlight"].get("title")
                ),
            }
        )

    return _respond(content)


def index_ocds(request):
    secret = request.GET.get("secret")
    version = request.GET.get("version")
    langs = request.GET.get("langs")

    error_message = None
    if not secret:
        error_message = "Need to supply secret"
    elif not version:
        error_message = "Need to supply version"
    elif not langs:
        error_message = "Need to supply langs"
    elif secret != settings.OCDS_SECRET:
        error_message = "secret not correct"

    if error_message:
        return _respond({"error": error_message})

    url = "https://standard.open-contracting.org/{}/".format(version)

    index_version = request.GET.get("index_version")
    if index_version:
        new_url = "https://standard.open-contracting.org/{}/".format(index_version)
    else:
        new_url = None

    for language_code in langs.split(","):
        language_code = language_code.strip()

        lang_url = _append_lang_code(url, language_code)
        if new_url:
            new_lang_url = _append_lang_code(new_url, language_code)
            base_url = new_lang_url
        else:
            new_lang_url = None
            base_url = lang_url

        results = process(lang_url, new_lang_url)
        _load(LANG_MAP.get(language_code, "standard"), base_url, results, language_code)

    return _respond({"success": True})
