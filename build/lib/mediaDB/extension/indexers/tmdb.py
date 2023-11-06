import tmdbsimple as tmdb
from json import load
from os.path import isfile
# relative imports
from mediaDB.common import *
from mediaDB.mediaTypes import *
from mediaDB.extension.Providers.common import ProviderCommon


class TMDB_manipulator(ProviderCommon):
    NAME:str
    SETTING_FILE: str
    CONFIG: dict
    API_KEY:str
    GENRE_MOVIE_FILE:str
    GENRE_TV_FILE:str

    NAME = "TMDB"
    CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/TMDB"
    SETTING_FILE = os.path.join(ProviderCommon.SETTING_DIRECTORY, NAME)
    VAR_DIRECTORY = os.path.join(ProviderCommon.VAR_DIRECTORY, NAME)
    CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
    GENRE_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, "genre_movie.json")
    GENRE_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, "genre_tv.json")
    if not isfile(SETTING_FILE) and not wget(CONFIG_EXEMPLE_URL, SETTING_FILE):
        raise ProviderConfigError
    CONFIG = parseConfig(SETTING_FILE)
    if not ProviderCommon.checkConfig(CONFIG, {"api_key": 1, "timeout": 1}):
        raise ProviderConfigError
    API_KEY = CONFIG["api_key"]

    tmdb.API_KEY = API_KEY
    tmdb.REQUESTS_TIMEOUT = CONFIG["timeout"]

    def download_genre():
        movie_list = tmdb.Genres().movie_list()
        tv_list = tmdb.Genres().tv_list()
        with open(TMDB_manipulator.GENRE_MOVIE_FILE, "w") as f:
            save_json(f, movie_list)
        with open(TMDB_manipulator.GENRE_TV_FILE, "w") as f:
            save_json(f, tv_list)

    download_genre()
    with open(GENRE_MOVIE_FILE, "r") as f:
        MOVIE_GENRE_IDS = load(f)
    with open(GENRE_TV_FILE, "r") as f:
        TV_GENRE_IDS = load(f)

    def genreExist(id:int, media_type:int):
        m, id_list = mediaType(media_type), None
        if m.have_season:
            id_list = TMDB_manipulator.TV_GENRE_IDS
        else:
            id_list = TMDB_manipulator.MOVIE_GENRE_IDS
        return id in [genre["id"] for genre in id_list["genres"]]


    def get(id:int, media_type:int) -> dict:
        if not isinstance(id, int):
            raise ValueError("method get: id must be int")
        
        

