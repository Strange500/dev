from mediaDB.exceptions import *
from mediaDB.common import *
class ProviderCommon():

    SETTING_DIRECTORY = os.path.join(CONF_DIR, "Indexers")
    VAR_DIRECTORY = os.path.join(VAR_DIR, "Indexers")
    PROXY = FlareSolverrProxy

    def make_result(tmdb_id:int, media_type:int, release_date:str, last_air_date:str | None = None, adult: bool | None = None, genres: list[int] | None = None, in_production: bool | None = False, last_episode_to_air: dict | None = None, title: str | None = None, other_titles:list[str] | None = None, next_episode_to_air: dict | None = None, number_of_episodes:int | None = None, number_of_season: int | None = None, original_language:str | None = None, seasons: dict | None = None, status: str | None = None) -> dict:
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
            raise ValueError("method make_result: release date cannot be None | release date need to be formatted as '%Y-%m-%d")

        if last_air_date is None:
            last_air_date = release_date

        if not isinstance(last_air_date, str) or not is_date_valid(last_air_date):
            raise ValueError("method make_result: last_air_date need to be formated as '%Y-%m-%d")
    
        if genres is None:
            genres = []

        if not isinstance(genres, list) : # add verif on genre ids
            raise ValueError("method make_result: genre has to be list of ints")
        
        for ids in genres:
            if not isinstance(ids, int):
                raise ValueError("method make_result: genre ids must be int")

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

        }


    def checkConfig(config: dict, keys: dict) -> bool:
        for key in keys:
            if config.get(key, None) is not None:
                if isinstance(config.get(key), dict) and isinstance(keys.get(key, None), dict) and not ProviderCommon.checkConfig(config[key], keys[key]):
                    return False
                continue
            else:
                return False
        return True

    