from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.Database import *
from mediaDB.flaresolver import *
from mediaDB.indexer import *
from mediaDB.mediaTypes import *
from mediaDB.metaProviders import *

from flask import Flask, jsonify, request, abort
from flask_cors import cross_origin

from json import load, dump

app = Flask(__name__)

@app.route("/provider/tv/get_info", methods=["POST"])
@cross_origin()
def getTVInfo():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    media_type = int(request.form.get("media_type"))
    if provider is not None and (id is not None or title is not None):
        if PROVIDERS_LIST.get(provider) is None:
            abort(401)
        p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
        if id is not None:
            return jsonify(p.getMediaData(tmdb_id=id))
        elif title is not None:
            return jsonify(p.getMediaData(title=title))
    return "ERROR"
