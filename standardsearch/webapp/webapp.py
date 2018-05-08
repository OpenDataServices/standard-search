import flask
import standardsearch.elasticsearchfactory

app = flask.Flask(__name__)


@app.route("/v1/search")
def hello():
    search = flask.request.args.get('q', '')

    elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()

    query = {"query": {"term": {"text": search}}, "highlight": {"fields": {"text": {}}}}

    res = elasticsearchfactory.get().search(index=elasticsearchfactory.index,
                                            body=query
                                            )

    out = {
        'results': [],
        'count': res['hits']['total'],
           }
    for hit in res['hits']['hits']:
        out['results'].append({
            "title": hit['_source']['title'],
            "url": hit['_source']['url'],
            "highlights": hit['highlight']['text'],
        })

    resp = flask.Response(flask.json.dumps(out), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
