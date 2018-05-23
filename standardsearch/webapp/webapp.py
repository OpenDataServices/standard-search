import flask
import standardsearch.elasticsearchfactory

app = flask.Flask(__name__)


@app.route("/v1/search")
def hello():
    search = flask.request.args.get('q', '')
    index = flask.request.args.get('index', 'standardsearch')

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

    resp = flask.Response(flask.json.dumps(out), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
