from mediaDB.common import *
from mediaDB.exceptions import *

class indexer():

    def __init__(self, name : str, indexer_manipulator: object) -> None:
        self.__name = name
        self.__manipulator = indexer_manipulator
        self.media_types = indexer_manipulator.media_types
        self.__var_directory = os.path.join(VAR_DIR, "indexers", self.__name)
        self.__conf_directory = os.path.join(CONF_DIR, "indexers", self.__name)

        pass

    def get_ep(self, title: str, episode : int, season : int, media_type: int):
        result = self.__manipulator.search_ep(media_type=media_type)
        if result is None:
            raise MediaNotFoundERROR
        else:
            return result
        
    def get_batch(self, title: str, season : int, media_type: int):
        result = self.__manipulator.search_ep(media_type=media_type)
        if result is None:
            raise MediaNotFoundERROR
        else:
            return result
        
    def get_show(self, title: str, episode : int, season : int, media_type: int):
        result = self.__manipulator.search_ep(media_type=media_type)
        if result is None:
            raise MediaNotFoundERROR
        else:
            return result
        
        