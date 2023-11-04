import os
import socket
import appdirs
import validators


from mediaDB.common import wget

DEBUG_MODE_ENABLE = False
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
APP_NAME = "mediaDB"
APP_AUTHOR = "Strange500"

VAR_DIR = appdirs.user_cache_dir(appname=APP_NAME, appauthor=APP_AUTHOR)
CONF_DIR = appdirs.user_config_dir(appname=APP_NAME, appauthor=APP_AUTHOR)
SETTINGS_DIR = os.path.join(CONF_DIR, "setting")


GENERAL_SETTINGS_FILE, __GENERAL_SETTINGS_URL = os.path.join(SETTINGS_DIR, "COMMON"),""
TMDB_MOVIE_BAN_FILE = os.path.join(SETTINGS_DIR, "banned_movies.list")
TMDB_TV_BAN_FILE = os.path.join(SETTINGS_DIR, "banned_tv.list")
INDEXERS_FILE, __INDEXERS_URL = os.path.join(SETTINGS_DIR,"Indexers.json"), ""
METADONNEE_PROVIDERS_FILE, __METADONNEE_PROVIDERS_URL = os.path.join(SETTINGS_DIR, "MetaProviders.json"), ""

os.makedirs(VAR_DIR, exist_ok=True)
os.makedirs(CONF_DIR, exist_ok=True)
os.makedirs(SETTINGS_DIR, exist_ok=True)

for couple in [(GENERAL_SETTINGS_FILE, __GENERAL_SETTINGS_URL), (TMDB_MOVIE_BAN_FILE, ""), (TMDB_TV_BAN_FILE, ""),
                  (INDEXERS_FILE, __INDEXERS_URL), (METADONNEE_PROVIDERS_FILE, __METADONNEE_PROVIDERS_URL)]:
    file, url = couple
    print(file)
    print(url)
    if not os.path.isfile(file) and validators.url(url):
        wget(url, file)
    else:
        with open(file, "w") as f:
            f.write("")