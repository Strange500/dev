import tmdbsimple as tmdb
from json import load
from os.path import isfile
from datetime import datetime
from thefuzz import process
from copy import deepcopy
# relative imports
from mediaDB.common import *
from mediaDB.mediaTypes import *
from mediaDB.extension.Providers.common import ProviderCommon
from mediaDB.settings import *
from about_time import about_time
class TMDB_manipulator(ProviderCommon):
    NAME:str
    SETTING_FILE: str
    CONFIG: dict
    API_KEY:str
    GENRE_MOVIE_FILE:str
    GENRE_TV_FILE:str
    IDS_MOVIE: dict
    IDS_TV: dict
    CACHE_DB_TV: dict
    CACHE_DB_MOVIE: dict
    with alive_bar(9, manual=True, title='Initializing tmdb provider', **bar_setting) as bar:
        # CONST
        __DATE = datetime.now().strftime("%m_%d_%Y")
        NAME = "TMDB"
        CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/TMDB"
        SETTING_FILE = os.path.join(ProviderCommon.SETTING_DIRECTORY, NAME)
        VAR_DIRECTORY = os.path.join(ProviderCommon.VAR_DIRECTORY, NAME)
        CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
        GENRE_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, "genre_movie.json")
        GENRE_TV_FILE = os.path.join(CACHE_DIRECTORY, "genre_tv.json")
        TMDB_EXPORT_URL = "https://files.tmdb.org/p/exports/"
        IDS_TV_FILE = os.path.join(CACHE_DIRECTORY, f"tv_ids_{__DATE}.json")
        IDS_TV_URL = f"{TMDB_EXPORT_URL}tv_series_ids_{__DATE}.json.gz"
        IDS_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, f"movies_ids_{__DATE}.json")
        IDS_MOVIES_URL = f"{TMDB_EXPORT_URL}movie_ids_{__DATE}.json.gz"
        CACHE_DB_TV_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv.json")
        CACHE_DB_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, "DB_movie.json")
        media_types = [1, 3]

        # CREATE NEEDED FILES & DIRECTORY
        os.makedirs(VAR_DIRECTORY, exist_ok=True)
        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
                # Download TMDB config file if not created
        if not isfile(SETTING_FILE) and not wget(CONFIG_EXEMPLE_URL, SETTING_FILE):
            raise ProviderConfigError
        if not isfile(CACHE_DB_TV_FILE) :
            with open(CACHE_DB_TV_FILE, "w", encoding="utf-8") as f:
                dump({}, f, indent=5)
        if not isfile(CACHE_DB_MOVIE_FILE) :
            with open(CACHE_DB_MOVIE_FILE, "w", encoding="utf-8") as f:
                dump({}, f, indent=5)
        # SETTING UP 
        CONFIG = parseConfig(SETTING_FILE)
        if not ProviderCommon.checkConfig(CONFIG, {"api_key": 1, "timeout": 1}):
            raise ProviderConfigError
        API_KEY = CONFIG["api_key"]
        tmdb.API_KEY = API_KEY[0]
        tmdb.REQUESTS_TIMEOUT = int(CONFIG["timeout"][0])
        bar(0.001)
            # Download tmdb ids file
        if not isfile(GENRE_MOVIE_FILE):
            movie_list = tmdb.Genres().movie_list()
            with open(GENRE_MOVIE_FILE, "w") as f:
                save_json(f, movie_list)
        bar(0.03)
        if not isfile(GENRE_TV_FILE):
            tv_list = tmdb.Genres().tv_list()
            with open(GENRE_TV_FILE, "w") as f:
                save_json(f, tv_list)
        bar(0.03)
        with open(GENRE_MOVIE_FILE, "r") as f:
            MOVIE_GENRE_IDS = load(f)
        with open(GENRE_TV_FILE, "r") as f:
            TV_GENRE_IDS = load(f)
        bar(0.001)
            # update ids files
        if not isfile(IDS_MOVIE_FILE) :

            if wget(IDS_MOVIES_URL, IDS_MOVIE_FILE+".gz"):
                gzExtract(IDS_MOVIE_FILE+".gz", IDS_MOVIE_FILE) 
                makeIdsFile(IDS_MOVIE_FILE)
        bar(0.59)
        if not isfile(IDS_TV_FILE) :
            if wget(IDS_TV_URL, IDS_TV_FILE+".gz"):
                gzExtract(IDS_TV_FILE+".gz", IDS_TV_FILE)    
                makeIdsFile(IDS_TV_FILE)
        bar(0.2)
            # loads ids
        with open(IDS_MOVIE_FILE, "r", encoding="utf-8") as f:
            IDS_MOVIE = load(f)
        bar(0.05)
        with open(IDS_TV_FILE, "r", encoding="utf-8") as f:
            IDS_TV = load(f)
        bar(0.009)
            # loads DB
        with open(CACHE_DB_TV_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_TV = load(f)
        with open(CACHE_DB_MOVIE_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_MOVIE = load(f)
        bar(1.)


    def genreExist(self, id:int, media_type:int):
        m, id_list = mediaType(media_type), None
        if m.have_season:
            id_list = self.TV_GENRE_IDS
        else:
            id_list = self.MOVIE_GENRE_IDS
        return id in [genre["id"] for genre in id_list["genres"]]
    
    def movieIdExist(self, id:int) -> bool:
        return self.IDS_MOVIE.get(f"{id}", None) is not None
    
    def tvIdExist(self, id:int) -> bool:
        return self.IDS_TV.get(f"{id}", None) is not None

    def getTitleTV(self, id: int) -> str:
        if self.tvIdExist(id):
            return self.IDS_TV[f"{id}"]
        
    def getTitleMovie(self, id: int) -> str:
        if self.movieIdExist(id):
            return self.IDS_MOVIE[f"{id}"]
        
    def __store_tmdb_tv_info(self, info_tmdb: dict):
        if (self.tvIdExist(info_tmdb["id"])):
            info = deepcopy(info_tmdb)
            id = info.pop("id")
            self.CACHE_DB_TV[f"{id}"] = info
            with open(self.CACHE_DB_TV_FILE, "w", encoding="utf-8") as f:
                dump(self.CACHE_DB_TV, f, indent=5, sort_keys=True)

    def __store_tmdb_movie_info(self, info_tmdb: dict):
        if (self.movieIdExist(info_tmdb["id"])):
            info = deepcopy(info_tmdb)
            id = info.pop("id")
            self.CACHE_DB_MOVIE[f"{id}"] = info
            with open(self.CACHE_DB_MOVIE_FILE, "w", encoding="utf-8") as f:
                dump(self.CACHE_DB_MOVIE, f, indent=5, sort_keys=True)

    # def __get_season_changes(self, changes_season: list[int], date:str)->dict:
    #     from pprint import pprint
    #     result = []
    #     for season_id in list(set(changes_season)):
    #         changes = tmdb.TV_Changes(season_id).season(start_date=date)["changes"]
    #         changes = [change["items"] for change in changes if change.get("items") is not None]
    #         changes = [change for change in changes if type(change) == list and len(change) > 0 and change[0]["value"].get("episode_id", None) is not None]
    #         if len(changes) > 0:
    #             changes = [item for change in changes for item in change]
    #         result = [*result, *[change["value"]["episode_id"] for change in changes if change.get("value", None) is not None and change["value"].get("episode_id") is not None ]]
            
    #     return 


    # def __get__changes_tv(self, info: dict) -> list[int] | None:
    #     date = info["info_date"]
    #     date = "2022-11-02"
    #     id = info["id"]
    #     result = []
    #     changes = tmdb.TV_Changes(id).series(start_date=date)["changes"]
    #     changes = [change["items"] for change in changes if change.get("items") is not None]
    #     changes = [change for change in changes if type(change) == list and len(change) > 0 and change[0]["value"].get("season_id", None) is not None]
    #     if len(changes) > 0:
    #         changes = [item for change in changes for item in change]
    #     for change in changes:
    #         value = change.get("value", None)
    #         if value is None:
    #             continue
    #         if dict(value).get("season_id", None) is not None:
    #             s_id = dict(value).get("season_id", None) 
    #             result.append(s_id)
    #     return self.__get_season_changes(result, date)

    def __get_info_from_cache_tv(self, id:int) -> dict|None:
        info = self.CACHE_DB_TV.get(f"{id}", None)
        if info is not None:
            date = datetime.strptime(info["info_date"], "%Y-%m-%d")
            if datetime.strptime(get_date(format="%Y-%m-%d"), "%Y-%m-%d")> date:
                return self.__getTVInfo(id)
            else:
                return info
        else:
            return info
        
    def __get_info_from_cache_movie(self, id:int) -> dict|None:
        info = self.CACHE_DB_MOVIE.get(f"{id}", None)
        if info is not None:
            date = datetime.strptime(info["info_date"], "%Y-%m-%d")
            if datetime.strptime(get_date(format="%Y-%m-%d"), "%Y-%m-%d")> date:                
                return self.__getMovieInfo(id)
            else:
                return info
        else:
            return info
        
    def findIdTV(self, title: str) -> int:
        titles = {self.IDS_TV[id]: id for id in self.IDS_TV}
        best, score = process.extractOne(title, [*titles])
        if score > 90:
            return int(titles[best])
        else:
            p = tmdb.Search()
            results_stat = p.tv(query=title)
            if results_stat["total_results"] > 0:
                return int(results_stat["results"][0]["id"])
            return -1
    
    def findIdMovie(self, title: str) -> int:
        titles = {self.IDS_MOVIE[id]: id for id in self.IDS_MOVIE}
        best, score = process.extractOne(title, [*titles])
        if score > 90:
            return int(titles[best])
        else:
            p = tmdb.Search()
            results_stat = p.movie(query=title)
            if results_stat["total_results"] > 0:
                return int(results_stat["results"][0]["id"])
            return -1
        
    def findTVByTitle(self, title: str) -> list[int]:
        return [info["id"] for info in tmdb.Search().tv(query=title)["results"] if info.get("id", None) is not None]
    
    def findMovieByTitle(self,title: str) -> list[int]:
        #print(tmdb.Search().movie(query=title) )
        return [info["id"] for info in tmdb.Search().movie(query=title)["results"] if info.get("id", None) is not None]
        
    def __make_seasons(self, info_tmdb:dict):
        id = info_tmdb["id"]
        if not self.tvIdExist(id):
            raise IdDoesNotExist(f"method __make_seasons: {id} does not exist")
        episode_group_id = [i for i in tmdb.TV(id).episode_groups()["results"] if i["name"] == "Seasons"]
        if episode_group_id == []:
            new_dic = {"seasons" : {}}
            season_data = info_tmdb["seasons"]
            for seasons in range(len(info_tmdb["seasons"])):
                air_date = season_data[seasons]["air_date"]
                episode_count = season_data[seasons]["episode_count"]
                episodes = [i for i in range(1, episode_count+1)]
                name = season_data[seasons]["name"]
                season_number = season_data[seasons]["season_number"]
                new_dic["seasons"][f"{season_number}"] = {
                            "air_date": air_date,
                            "episode_count": episode_count,
                            "name": name,
                            "episodes_list": episodes
                    }
            info_tmdb["number_of_season"] = len(new_dic["seasons"])
            info_tmdb["seasons"] = new_dic["seasons"]
            return info_tmdb
        episode_group_id = episode_group_id[0]["id"]
        new_dic = {"seasons" : {}}
        info = tmdb.TV_Episode_Groups(id=episode_group_id).info()['groups']
        for seasons in range(len(info)):
            air_date = info[seasons]['episodes'][0]["air_date"]
            episode_count = len(info[seasons]['episodes'])
            episodes = [ep_data["episode_number"] for ep_data in info[seasons]['episodes'] if ep_data.get("episode_number") is not None]
            name = info[seasons]["name"]
            season_number = info[seasons]["order"]
            new_dic["seasons"][f"{season_number}"] = {
                        "air_date": air_date,
                        "episode_count": episode_count,
                        "name": name,
                        "episodes_list": episodes
                }
        info_tmdb["number_of_season"] = len(info)
        info_tmdb["seasons"] = new_dic["seasons"]
        return info_tmdb
    
    def __alter_title_translations(self, info_tmdb: dict) -> dict:
        result = []
        tr = info_tmdb.get("translations", None)
        if tr is not None:
            try:
                tr = [trans["data"]["title"] for trans in tr["translations"] if trans["data"]["title"] != '' and is_latin(trans["data"]["title"]) ]
            except KeyError:
                tr = [trans["data"]["name"] for trans in tr["translations"] if trans["data"]["name"] != '' and is_latin(trans["data"]["name"]) ]
            for title in tr:
                result.append({"title": title})
        return result
            
    
    def __make_alter_titles(self, info_tmdb: dict) -> dict:
        if info_tmdb.get("media_type") == 3:
            alter = tmdb.tv.TV(info_tmdb['id']).alternative_titles()["results"]
            alter = [*alter, *self.__alter_title_translations(info_tmdb)]
        elif info_tmdb.get("media_type") == 1:
            alter = tmdb.movies.Movies(info_tmdb['id']).alternative_titles()["titles"]
            alter = [*alter, *self.__alter_title_translations(info_tmdb)]
        result = []
        for dic in alter:
            title = dic["title"]
            if is_latin(title) and title != '':
                result.append(title)
        if info_tmdb.get("name", None) is not None and is_latin(info_tmdb.get("name")) :
            result.append(info_tmdb.get("name", ""))
        if info_tmdb.get("original_name", None) is not None and is_latin(info_tmdb.get("original_name")) :
            result.append(info_tmdb.get("original_name", ""))
        info_tmdb["other_titles"] = list(set(result))
        return info_tmdb
        
    def __make_release_date(self, tmdb_info: dict) -> dict:
        if tmdb_info.get("release_date", None) is None and not tmdb_info.get("first_air_date", None) in [None, ""]:
            tmdb_info["release_date"] = tmdb_info["first_air_date"]
        elif (tmdb_info.get("release_date", None) in [None, ""] or not is_date_valid(tmdb_info.get("release_date", None))) and not tmdb_info.get("first_air_date", None) in [None, ""]:
            tmdb_info["release_date"] = tmdb_info["first_air_date"]
        else:
            tmdb_info["release_date"] = "2004-08-12"
        return tmdb_info
    
    def __make_genres(self, tmdb_info: dict) -> dict:
        if len([type(item) for item in tmdb_info["genres"] if type(item) == int]) > 0:
            return tmdb_info
        tmdb_info["genres"] = [genre_data["id"] for genre_data in tmdb_info["genres"] if genre_data.get("id", None) is not None]
        return tmdb_info
    
    def __make_tmdb_id(self, tmdb_info: dict) -> dict:
        tmdb_info["tmdb_id"] = tmdb_info["id"]
        return tmdb_info

    def __make_last_episode_to_air(self, tmdb_info:dict) -> dict:
        if tmdb_info.get("last_episode_to_air", None) is None:
            tmdb_info["last_episode_to_air"] = None
            return tmdb_info
        else:
            ep_info = tmdb_info["last_episode_to_air"]
            tmdb_info["last_episode_to_air"] = {
                "air_date" : ep_info["air_date"],
                "episode_number": ep_info["episode_number"],
                "season_number": ep_info["season_number"]
            }
            return tmdb_info
        
    def __make_next_episode_to_air(self, tmdb_info:dict) -> dict:
        if tmdb_info.get("next_episode_to_air", None) is None:
            tmdb_info["next_episode_to_air"] = None
            return tmdb_info
        else:
            ep_info = tmdb_info["next_episode_to_air"]
            tmdb_info["next_episode_to_air"] = {
                "air_date" : ep_info["air_date"],
                "episode_number": ep_info["episode_number"],
                "season_number": ep_info["season_number"]
            }
            return tmdb_info
        
    def __make_title(self, tmdb_info:dict)-> dict:
        if tmdb_info.get("title", None) is not None:
            return tmdb_info
        elif tmdb_info.get("name", None) is not None:
            tmdb_info["title"] = tmdb_info["name"]
            return tmdb_info
        else:
            raise MalformedTMDBInfo
        
    def __formatTV_info(self, info:dict) -> dict:
        info["media_type"] = 3
        info = self.__make_seasons(info)
        info = self.__make_alter_titles(info)
        info = self.__make_genres(info)
        info = self.__make_last_episode_to_air(info)
        info = self.__make_release_date(info)
        info = self.__make_title(info)
        info = self.__make_tmdb_id(info)
        info = self.__make_next_episode_to_air(info)
        if info.get("status", None) is None:
            info["status"] = "Ended"
        return info
    
    def __formatMovieInfo(self, info: dict) -> dict:
        info["media_type"] = 1
        info = self.__make_alter_titles(info)
        print(info.get("other_titles", None))
        info = self.__make_genres(info)
        info = self.__make_last_episode_to_air(info)
        info = self.__make_release_date(info)
        info = self.__make_title(info)
        info = self.__make_tmdb_id(info)
        info = self.__make_next_episode_to_air(info)
        info["seasons"] = None
        if info.get("status", None) is None:
            info["status"] = "Ended"
        return info

    def __get_tmdb_info_tv(self, id, append_to_response:str | None = "seasons,translations") -> dict:
        return tmdb.tv.TV(id).info(append_to_response=append_to_response)
                                   
    def __get_tmdb_info_movie(self, id, append_to_response:str | None = "translations") -> dict:
        return tmdb.movies.Movies(id).info(append_to_response=append_to_response)
                                   
    def __getTVInfo(self, id: int) -> dict:
        if not self.tvIdExist(id):
            raise IdDoesNotExist(f"method getTVInfo: {id} does not exist")
        info = self.__get_tmdb_info_tv(id)
        info["info_date"] = get_date(format="%Y-%m-%d")
        info["id"] = id
        info = self.__formatTV_info(info)
        self.__store_tmdb_tv_info(info)
        return info
    
    def __getMovieInfo(self, id: int) -> dict:
        if not self.movieIdExist(id):
            raise IdDoesNotExist(f"method getMovieInfo: {id} does not exist")
        info = self.__get_tmdb_info_movie(id)
        info["info_date"] = get_date(format="%Y-%m-%d")
        info["id"] = id
        info = self.__formatMovieInfo(info)
        self.__store_tmdb_movie_info(info)
        return info

    def get(self, id:int, media_type:int) -> dict:
        #print(id, media_type)
        if not isinstance(id, int):
            raise ValueError("method get: id must be int")
        if media_type == 1:
            return ProviderCommon.make_result(**self.__getMovieInfo(id))
        if media_type == 3:
            return ProviderCommon.make_result(**self.__getTVInfo(id))
        
    def find(self, title:int, media_type:int) -> dict:
        if not isinstance(title, str):
            raise ValueError("method get: tile must be str")
        result = []
        if media_type == 1:
            for ids in self.findMovieByTitle(title=title):
                info = self.__get_info_from_cache_movie(ids)
                if info is None:
                    result.append(ProviderCommon.make_result(**self.__getMovieInfo(ids)))
                else:
                    result.append(ProviderCommon.make_result(**info))                  
        elif media_type == 3:
            for ids in self.findTVByTitle(title=title):
                info = self.__get_info_from_cache_tv(ids)
                if info is None:
                    result.append(ProviderCommon.make_result(**self.__getTVInfo(ids)))
                else:
                    result.append(ProviderCommon.make_result(**info))

        return result
        

    
        
        

