from mediaDB.common import *
from mediaDB.Database import *
from mediaDB.flaresolver import *
from mediaDB.indexer import *
from mediaDB.mediaTypes import *
from mediaDB.metaProviders import *

from flask import Flask, jsonify, request, abort
from flask_cors import cross_origin

from json import load, dump

app = Flask(__name__)

@app.route("/mediatypes/add", methods=["POST"])
@cross_origin()
def addMediaType():
    if request.method == "POST" and  request.form.get("name", None) is not None:
        
        have_season = False
        if request.form.get("have_season", None) is not None:
            have_season = True


        name = request.form.get("name", None)
        with open(MEDIA_TYPES_FILE, "r", encoding="utf-8") as f:
            media_types_json = load(f)
        if key_value_in_dic_key(media_types_json, "name", name):
            return jsonify(make_response_api(False, "Media type already exist"))
        else:
            createMediaType(name, have_season=have_season)
            return jsonify(make_response_api(True, f"Media created"))
                
@app.route("/mediatypes/delete", methods=["POST"])
@cross_origin()
def deleteMediaType():
    if request.method == "POST" and  request.form.get("id", None) is not None:
        id = request.form.get("id", None)
        with open(MEDIA_TYPES_FILE, "r", encoding="utf-8") as f:
            media_types_json = dict(load(f))
        if key_value_in_dic_key(media_types_json, f"{id}", str(id)):
            media_types_json.pop(str(id))
            with open(MEDIA_TYPES_FILE, "w") as f:
                dump(media_types_json, f)
            return jsonify(make_response_api(True, f"Media with id {id} deleted"))
        else:
            return jsonify(make_response_api(False, f"Media with id {id} does not exist"))