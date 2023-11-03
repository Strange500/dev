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
from datetime import datetime
# if platform.system() == "Linux":
#     import psutil
# elif platform.system() == "Windows":
#     import wmi


from mediaDB.flaresolver import FlareSolverrProxy

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

def forbidden_car(name):
    """
    Removes forbidden characters from a file name.

    Args:
        name (str): The file name to be processed.

    Returns:
        str: The processed file name with forbidden characters removed.

    Example:
        >>> forbidden_car("file?name")
        'filename'
    """
    for car in ["?", '"', "/", "\\", "*", ":", "<", ">", "|"]:
        name = name.replace(car, "")
    return name

def is_video(file_path):
    """
    Checks if a file at the given path is a video file.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is a video file, False otherwise.
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv']
    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in video_extensions

def is_connected() -> bool:
    try:
        requests.get("https://google.com")
    except requests.exceptions.ConnectionError:
        return False
    return True

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

def parseConfig(file_path) -> dict:
        """bonjour"""
        try:
            config = {}
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line[0] in ["#", "\n", ""]:
                        continue
                    line = line.replace("\n", "").split(" = ")
                    if "," in line[1]:
                        line[1] = [elt.strip() for elt in line[1].split(",")]
                    else:
                        line[1] = [line[1].strip()]
                    arg1, arg2 = line[0].strip(), line[1]
                    config[arg1] = arg2

            return config
        except IOError:
            return 
        

def is_date_valid(date_string, format='%Y-%m-%d'):
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False
    
def save_json(f, obj: dict):
    dump(obj, f, indent=5)
        
if __name__ == '__main__':
    from pprint import pprint
    pprint(parseConfig("test.pyc"))