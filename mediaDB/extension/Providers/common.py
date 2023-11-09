from mediaDB.exceptions import *
from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.mediaTypes import mediaType
class ProviderCommon():

    # VARIABLES
    SETTING_DIRECTORY = os.path.join(CONF_DIR, "Indexers")
    VAR_DIRECTORY = os.path.join(VAR_DIR, "Indexers")
    PROXY = FlareSolverrProxy

    # CREATING FILES & DIRECTORIES
    os.makedirs(SETTING_DIRECTORY, exist_ok=True)
    os.makedirs(VAR_DIRECTORY, exist_ok=True)
    

    def make_result(tmdb_id:int, media_type:int, release_date:str, last_air_date:str | None = None, adult: bool | None = None, genres: list[int] | None = None, in_production: bool | None = False, last_episode_to_air: dict | None = None, title: str | None = None, other_titles:list[str] | None = None, next_episode_to_air: dict | None = None, number_of_episodes:int | None = None, number_of_season: int | None = None, original_language:str | None = None, seasons: dict | None = None, status: str | None = None, info_date: str|None= None, **kwargs) -> dict:
        """
        Normalize data, in order to be used by metaProvider.py
        {
            "adult": bool,
            "release_date": string,
            "last_air_date": string,
            "genres": [int],
            "tmdb_id": int,
            "in_production": bool,
            "last_episode_to_air": {
                "air_date" : string,
                "episode_number": int,
                "season_number": int
            },
            "title": string,
            "other_titles": [string],
            "next_episode_to_air": {
                "air_date" : string,
                "episode_number": int,
                "season_number": int
            },
            "number_of_episodes": int,
            "number_of_season": int,
            "media_type": int,
            "original_language": string,
            "seasons": {
                "1": {
                    "air_date": string,
                    "episode_count": int,
                    "name": string,
                    "episodes_list": [int]
                    }
                },
            "status": string,

        }"""
        if adult is None:
            adult = False

        if release_date is None or not isinstance(release_date, str) or not is_date_valid(release_date):
            print(release_date)
            raise ValueError("method make_result: release date cannot be None | release date need to be formatted as '%Y-%m-%d")

        if last_air_date is None:
            last_air_date = release_date

        if not isinstance(last_air_date, str) or not is_date_valid(last_air_date):
            raise ValueError("method make_result: last_air_date need to be formated as '%Y-%m-%d")
    
        if genres is None:
            genres = []

        if not isinstance(genres, list) or not itemsAreType(genres, int): 
            raise ValueError("method make_result: genre has to be list of ints")
        
        for ids in genres:
            if not isinstance(ids, int):
                raise ValueError("method make_result: genre ids must be int")
            
        if not isinstance(tmdb_id, int):
            raise ValueError("method make_results: tmdb_id has to be int")

        if not isinstance(in_production, bool):
            raise ValueError("method make_results: in_production has to be bool")
        
        if not isinstance(last_episode_to_air, dict) and not last_episode_to_air is None:
            print(isinstance(last_episode_to_air, dict))
            raise ValueError("method make_results: last_episode_to_air has to be dict or None")
        
        if not isinstance(title, str):
            raise ValueError("method make_results: title has to be str")
        
        if not isinstance(other_titles, list) or not itemsAreType(other_titles, str):
            raise ValueError("method make_results: other_titles has to be list and items are str")
        
        if (not isinstance(number_of_episodes, int) or number_of_episodes < 0) and number_of_episodes is not None:
            raise ValueError("method make_results: number_of_episodes has to be int and > 0")
        
        if (not isinstance(number_of_season, int) or number_of_season < 0) and number_of_season is not None:
            raise ValueError("method make_results: number_of_seasons has to be int and > 0")
        try:
            mediaType(media_type)
        except MediaTypeDoesNotExist:
            raise ValueError("method make_results: media_type has to be int and exist for MediaType class")
        
        if not isinstance(original_language, str):
            raise ValueError("method make_results: original_language has to be str")
        
        if not isinstance(seasons, dict) and not seasons is None:
            raise ValueError("method make_results: seasons has to be list or None")
        
        if not isinstance(status, str):
            raise ValueError("method make_results: status has to be str")
        
        if not isinstance(info_date, str) or not is_date_valid(info_date):
            raise ValueError("method make_results: info_date has to be str and valid date (%Y-%m-%d)")
        
        
        result = {
            "adult": adult,
            "release_date": release_date,
            "last_air_date": release_date,
            "genres": genres,
            "tmdb_id": tmdb_id,
            "in_production": in_production,
            "last_episode_to_air": last_episode_to_air,
            "title": title,
            "other_titles": other_titles,
            "next_episode_to_air": next_episode_to_air,
            "number_of_episodes": number_of_episodes,
            "number_of_season": number_of_season,
            "media_type": media_type,
            "original_language": original_language,
            "seasons": seasons,
            "status": status,
            "info_date": info_date

        }
        return result


    def checkConfig(config: dict, keys: dict) -> bool:
        for key in keys:
            if config.get(key, None) is not None:
                if isinstance(config.get(key), dict) and isinstance(keys.get(key, None), dict) and not ProviderCommon.checkConfig(config[key], keys[key]):
                    return False
                continue
            else:
                return False
        return True

    
