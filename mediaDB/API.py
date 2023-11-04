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

