import os
import socket
import appdirs
from urllib.parse import urlparse
import validators
import gzip
import shutil
from copy import deepcopy
import requests
import re
import sys
from json import dump, load, loads, JSONDecodeError
from datetime import datetime
from alive_progress import alive_bar
# local imports
from mediaDB.flaresolver import FlareSolverrProxy

bar_setting = {"bar" :"classic2", "spinner":"pulse"}

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


        
def create_config_file(file_path:str, content: str):
    with open(file_path, "w") as f:
        f.write(file_path)

def wget(url: str, save_path: str) -> bool:
    try:
        response = requests.get(url)
    except requests.RequestException:
        return False
    try:
        with open(save_path, "wb") as f:
            f.write(bytes(response.content))
    except IOError:
        return False
    return True

def gzExtract(gz_file:str, file_name:str):
    with gzip.open(gz_file, 'rb') as f_in:
        with open(file_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(gz_file)

def makeIdsFile(path:str):
    dic = {}
    with open(path, "r", encoding="utf-8") as f:
        for lines in f:
            try:
                js = loads(lines)
            except JSONDecodeError:
                continue
            if js.get("id", None) is None:
                continue
            if js.get("original_title", None) is None and js.get("original_name", None) is None:
                continue
            try:
                dic[js["id"]] = js["original_title"]
            except KeyError:
                dic[js["id"]] = js["original_name"]
    with open(path, "w") as f:
        dump(dic, f, indent=5)

def is_latin(chaine):
    motif = re.compile(r'[^a-zA-ZÀ-ÿ\s!@#$%^&*()_\-+=\[\]{};:\'",.<>/?\\|`~]+')
    return not motif.search(chaine)

def get_date(format: str|None = "%m_%d_%Y"):
    return datetime.now().strftime(format)

def itemsAreType(items: list, tp) -> bool:
    for item in items:
        if not isinstance(item, tp):
            return False
    return True


def get_current_time():
    current_time = datetime.now().strftime("%H:%M")
    return current_time

def update_progress_bar(msg:str, progress:int):
    bar_length = 20
    block = int(round(bar_length * progress))
    progress_str = f"\r[{block * '#' + (bar_length - block) * '-'}] {msg}"
    print(progress_str, end='', flush=True)