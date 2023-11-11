from alive_progress import alive_bar
import re

from mediaDB.extension.Parsers.common import ParserCommon
from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.extension.Providers.tmdb import TMDB_manipulator


class ParserTV(ParserCommon):
    """{
        "pattern": "^(?:\\[(?P<source>.+?)\\]\\s*)?(?P<title>.+?)([\\._ ]*| - )S(?P<season>\\d{1,2})E(?P<episode>\\d{1,4})",
        
        }
        """
    SOURCES:dict


    # CONST
    NAME = "TV"
    CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/TV"
    SETTING_DIRECTORY = os.path.join(ParserCommon.SETTING_DIRECTORY, NAME)
    SETTING_FILE = os.path.join(SETTING_DIRECTORY, NAME)
    VAR_DIRECTORY = os.path.join(ParserCommon.CACHE_DIRECTORY, NAME)
    CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
    SOURCE_DIRECTORY = os.path.join(SETTING_DIRECTORY, "sources")
    SOURCES = dict()
    media_types = [3]

    os.makedirs(SETTING_DIRECTORY, exist_ok=True)
    os.makedirs(VAR_DIRECTORY, exist_ok=True)
    os.makedirs(CACHE_DIRECTORY, exist_ok=True)
    os.makedirs(SOURCE_DIRECTORY, exist_ok=True)

    for sources in os.listdir(SOURCE_DIRECTORY):
        with open(os.path.join(SOURCE_DIRECTORY, sources), "r") as f:
            SOURCES[sources] = load(f)

    def __init__(self, source_name:str) -> None:
        self.patterns = self.SOURCES.get(source_name)
        if self.patterns is not None:
            self.patterns = self.patterns["patterns"]

    def getTVAttribute(self,filename:str, source:str|None=None, is_batch: bool|None=False) -> dict:
        result = dict()

        if self.patterns is not None:
            regexp_resut = None
            if is_batch and self.patterns.get("batch", None) is not None:
                regexp_resut = re.match(self.patterns.get("batch"), filename)
            elif not is_batch and self.patterns.get("episode", None) is not None:
                regexp_resut = re.match(self.patterns.get("episode"), filename)
            if regexp_resut is not None:
                d = regexp_resut.groupdict()
                return {key:d[key] for key in d if d.get(key) is not None}
            return {}

        return result
    
    # def getEpisodeNumber(self, filename:str) -> tuple[int,int]:
    #     return TMDB_manipulator().bestMatchTV(filename)

