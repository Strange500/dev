# import ctypes
# import datetime
# import json
import os
import platform
# import shutil
import socket
# import time
from typing import Dict, Union
from urllib.parse import urlparse, quote
import appdirs
# import requests
from urllib.parse import urlparse
# import tmdbsimple as tmdb
# from thefuzz import process
# import re
from copy import deepcopy

import requests
from json import dump
# if platform.system() == "Linux":
#     import psutil
# elif platform.system() == "Windows":
#     import wmi


from flaresolver import FlareSolverrProxy

DEBUG_MODE_ENABLE = False

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

APP_NAME = "Media-Manager"
APP_AUTHOR = "Strange500"

VAR_DIR = appdirs.user_cache_dir(appname=APP_NAME, appauthor=APP_AUTHOR)
CONF_DIR = appdirs.user_config_dir(appname=APP_NAME, appauthor=APP_AUTHOR)


BAN_IDs_FILE = os.path.join(CONF_DIR, "settings", "list_ban_id.list")
MEDIA_TYPES_FILE = os.path.join(CONF_DIR, "setting", "MediaTypes.json")
INDEXERS_FILE = os.path.join(CONF_DIR, "setting", "Indexers.json")
METADONNEE_PROVIDERS_FILE = os.path.join(CONF_DIR, "setting", "MetaProviders.json")









os.makedirs(VAR_DIR, exist_ok=True)
os.makedirs(CONF_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)



def key_value_in_dic_key(dic: dict, key: str, value) -> bool:
    for ids in dic:
        val = dic[ids].get(key, None)
        if val == value:
            return True
    return False

def make_response_api(status : bool, detail: str):
    response = "ok"
    if not status:
        response = "failed"
    return {"status": response,
            "detail": detail}

def next_id(dic: dict) -> int:
    max_id = -1
    for key in dic:
        key = str(key)
        if key.isnumeric() and max_id < int(key):
            max_id = int(key)
    return max_id + 1

