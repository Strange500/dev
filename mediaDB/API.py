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

######## METAPROVIDER ##########

@app.route("/provider/tv/get_info", methods=["POST"])
@cross_origin()
def getTVInfo():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    media_type = 3
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.getMediaData(tmdb_id=int(id)))
    elif title is not None:
        return jsonify(p.getMediaData(title=title))
    return "ERROR"

@app.route("/provider/tv/exist", methods=["POST"])
@cross_origin()
def TVExist():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    media_type = 3
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.mediaExistbyId(int(id)))
    elif title is not None:
        return jsonify(p.mediaExistbyName(title=title))
    return "ERROR"


@app.route("/provider/tv/season/get_info", methods=["POST"])
@cross_origin()
def getTVSeasonInfo():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    season = request.form.get("season")
    media_type = 3
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))
            and canConvertInt(season)):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.getSeasonInfo(tmdb_id=int(id), season=season))
    elif title is not None:
        return jsonify(p.getSeasonInfo(title=title, season=season))
    return "ERROR"

@app.route("/provider/tv/season/exist", methods=["POST"])
@cross_origin()
def TVSeasonExist():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    season = request.form.get("season")
    media_type = 3
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))
            and canConvertInt(season)):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.seasonExistbyId(id=id, season=season))
    elif title is not None:
        return jsonify(p.seasonExistbyName(title=title, season=season))
    return "ERROR"

@app.route("/provider/tv/episode/exist", methods=["POST"])
@cross_origin()
def TVEpisodeExist():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    season = request.form.get("season")
    episode = request.form.get("episode")
    media_type = 3
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))
            and canConvertInt(season) and canConvertInt(episode)):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.episodeExistbyId(id=id, season=season, episode=episode))
    elif title is not None:
        return jsonify(p.episodeExistbyName(title=title, season=season, episode=episode))
    return "ERROR"



@app.route("/provider/movie/get_info", methods=["POST"])
@cross_origin()
def getMovieInfo():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    media_type = 1
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.getMediaData(tmdb_id=int(id)))
    elif title is not None:
        return jsonify(p.getMediaData(title=title))
    return "ERROR"

@app.route("/provider/movie/exist", methods=["POST"])
@cross_origin()
def MovieExist():
    provider = request.form.get("provider")
    id = request.form.get("id")
    title = request.form.get("title")
    media_type = 1
    if not (isinstance(provider, str) and (canConvertInt(id) or isinstance(title, str))):
        abort(400)
    if PROVIDERS_LIST.get(provider) is None:
        abort(400)
    p = MetaProviders(provider, PROVIDERS_LIST.get(provider), media_type)
    if id is not None:
        return jsonify(p.mediaExistbyId(int(id)))
    elif title is not None:
        return jsonify(p.mediaExistbyName(title=title))
    return "ERROR"


