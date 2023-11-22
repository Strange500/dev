from mediaDB.common import *
from mediaDB.exceptions import *
from mediaDB.settings import *
from mediaDB.extension.Indexers.Yggtorrent import Yggtorrent_manipulator

class indexer():

    def __init__(self, name : str, indexer_manipulator: object) -> None:
        self.__name = name
        if callable(indexer_manipulator):
            self.__manipulator = indexer_manipulator()
        else:
            raise ValueError
        self.__var_directory = os.path.join(VAR_DIR, "indexers", self.__name)
        self.__conf_directory = os.path.join(CONF_DIR, "indexers", self.__name)

        pass

    def get_ep(self, titles: str|list[str], episode : int, season : int):
        if hasattr(self.__manipulator, "get_ep"):
            result = self.__manipulator.get_ep(titles=titles, episodes=episode, seasons=season)
            if result is None:
                raise MediaNotFoundERROR
            else:
                return result
        
    def get_batch(self, titles: str|list[str], season : int):
        if hasattr(self.__manipulator, "get_batch"):
            result = self.__manipulator.get_batch(titles=titles, seasons=season)
            if result is None:
                raise MediaNotFoundERROR
            else:
                return result
        
    def get_movie(self, titles: str|list[str]):
        if hasattr(self.__manipulator, "get_movie"):
            result = self.__manipulator.get_movie(titles=titles)
            if result is None:
                raise MediaNotFoundERROR
            else:
                return result
            
    def downloadTorrent(self, torrent_id, savePath:str) -> None:
        if hasattr(self.__manipulator, "donwload"):
            content = self.__manipulator.download(torrent_id)
            with open(savePath, "w", encoding="utf-8") as f:
                f.write(content)

    
        
        
        