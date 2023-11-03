from common import *
from exceptions import *
from thefuzz import process

class MetaProviders():
    """All MetaProviders must return metadata as the foolowing dictionnary :
    result = {
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

    def __init__(self, name: str, provider_manipulator : object, media_type : int) -> None:
        self.__name = name
        self.__manipulator = provider_manipulator
        self.__media_types = provider_manipulator.media_types
        if media_type not in self.__media_types:
            raise MediaTypeNotSupported
        self.__media_type = media_type

    def mediaExistbyName(self, title: str):
        results = self.__manipulator.find(title, self.__media_type)
        r, score = process.extractOne(title, [result["title"] for result in results])
        if score > 90:
            return True
        else:
            return False
        

    def seasonExistbyName(self, title: str, season: int) -> bool:
        if self.mediaExistbyName(title):
            data = self.getMediaData(title=title)
            return season in [int(s) for s in data["seasons"]]
        else:
            return False

    def episodeExistbyName(self, title : str, season: int, episode: int) -> bool:
        if self.mediaExistbyName(title) and self.seasonExist(title, season=season):
            data = self.getMediaData(title=title)
            s = dict(data["seasons"]).get(f"{season}", None)
            if s is None:
                return False
            else:
                return episode in s["episodes_list"]
            
    def mediaExistbyId(self, identifier: int):
        result = self.__manipulator.get(identifier, self.__media_type)
        return result is None
        

    def seasonExistbyId(self, id: int, season: int) -> bool:
        if self.mediaExistbyId(id):
            data = self.getMediaData(tmdb_id=id)
            return season in [int(s) for s in data["seasons"]]
        else:
            return False

    def episodeExistbyName(self, id : int, season: int, episode: int) -> bool:
        if self.mediaExistbyId(id) and self.seasonExistbyId(id, season=season):
            data = self.getMediaData(tmdb_id=id)
            s = dict(data["seasons"]).get(f"{season}", None)
            if s is None:
                return False
            else:
                return episode in s["episodes_list"]


    def getMediaData(self, title:str|None = None, tmdb_id:int | None = None) -> dict:
        if (title is None and tmdb_id is None) or (title is not None and tmdb_id is not None):
            raise ValueError("methods getMediaData: you must use title or (xor) tmdb_id")
        if title is not None:
            if not isinstance(title, str):
                raise ValueError("methods getMediaData: title has to be instance of str")
            if not self.mediaExistbyName(title):
                return None
            list_results = self.__manipulator.find(title, self.__media_type)
            list_titles = [result["title"] for result in list_results]
            title, score = process.extractOne(title, list_titles)
            if score > 90:
                return list_results[list_titles.index(title)]
            return None
        elif tmdb_id is not None:
            if not isinstance(tmdb_id, int):
                raise ValueError("methods getMediaData: tmdb_id has to be instance of int")
            if not self.mediaExistbyId(tmdb_id):
                return None
            return self.__manipulator.get(id, self.__media_type)
        
    def getSeasonInfo(self, season: int, title: str | None = None, tmdb_id: int | None = None) -> dict:
        if (title is None and tmdb_id is None) or (title is not None and tmdb_id is not None):
            raise ValueError("methods getSeasonInfo: you must use title or (xor) tmdb_id")
        if title is not None:
            if not isinstance(title, str):
                raise ValueError("methods getSeasonInfo: title has to be instance of str")
            if not self.seasonExistbyName(title, season):
                return None
            list_results = self.__manipulator.find(title, self.__media_type)
            list_titles = [result["title"] for result in list_results]
            title, score = process.extractOne(title, list_titles)
            if score > 90:
                media_info = list_results[list_titles.index(title)]
                return media_info["seasons"][f"{season}"]
            return None
        elif tmdb_id is not None:
            if not isinstance(tmdb_id, int):
                raise ValueError("methods getMediaData: tmdb_id has to be instance of int")
            if not self.seasonExistbyId(tmdb_id):
                return None
            return self.__manipulator(id, self.__media_type)["seasons"][f"{season}"]
        
        