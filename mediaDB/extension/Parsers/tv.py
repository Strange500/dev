from alive_progress import alive_bar
import re
import typing

from mediaDB.extension.Parsers.common import ParserCommon,source_type,sources_type,dict_pattern_type
from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.extension.Providers.tmdb import TMDB_manipulator


class ParserVideo(ParserCommon):
    """{
        "pattern": "^(?:\\[(?P<source>.+?)\\]\\s*)?(?P<title>.+?)([\\._ ]*| - )S(?P<season>\\d{1,2})E(?P<episode>\\d{1,4})",
        
        }
        """
    SOURCES:sources_type


    # CONST
    NAME = "TV"
    CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/TV"
    SETTING_DIRECTORY = os.path.join(ParserCommon.SETTING_DIRECTORY, NAME)
    SETTING_FILE = os.path.join(SETTING_DIRECTORY, NAME)
    VAR_DIRECTORY = os.path.join(ParserCommon.CACHE_DIRECTORY, NAME)
    CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
    SOURCE_DIRECTORY = os.path.join(SETTING_DIRECTORY, "sources")
    SOURCES = dict()
    media_types = [1, 3]

    os.makedirs(SETTING_DIRECTORY, exist_ok=True)
    os.makedirs(VAR_DIRECTORY, exist_ok=True)
    os.makedirs(CACHE_DIRECTORY, exist_ok=True)
    os.makedirs(SOURCE_DIRECTORY, exist_ok=True)

    for sources in os.listdir(SOURCE_DIRECTORY):
        with open(os.path.join(SOURCE_DIRECTORY, sources), "r") as f:
            try:
                SOURCES[sources] = load(f)
            except JSONDecodeError:
                pass

    def __init__(self, source_name:str) -> None:

        self.patterns:dict_pattern_type
        self.source_name:str
        self.source: source_type
        self.source_name = source_name
        self.source = self.SOURCES.get(source_name)
        if self.source is not None:
            self.patterns = self.source.get("patterns", None)

    def __test_all_patterns(self, filename:str, patterns:list[str]|None) -> re.Match[str] | None:
        if patterns is None:
            return None
        regexp, cpt = None, 0
        while cpt < len(patterns) and regexp is None:
            regexp = re.match(patterns[cpt], filename)
            cpt = cpt + 1
        return regexp



    def getTVAttribute(self,filename:str, source:str|None=None, is_batch: bool|None=False) -> dict:
        result = dict()

        if self.patterns is not None:
            regexp_resut = None
            if is_batch and self.patterns.get("batch", None) is not None:
                regexp_resut = self.__test_all_patterns(filename, self.patterns.get("batch", None))
            elif not is_batch and self.patterns.get("episode", None) is not None:
                regexp_resut = self.__test_all_patterns(filename, self.patterns.get("episode", None))
            if regexp_resut is not None:
                d = regexp_resut.groupdict()
                return {key:d[key] for key in d if d.get(key) is not None}
            return {}
        return result
    
    def addSource(self, ep_pattern:list[str]|None=None, batch_pattern:list[str]|None=None, movie_pattern:list[str]|None=None) ->None:
        with open(os.path.join(self.SOURCE_DIRECTORY, self.source_name), "w", encoding="utf-8") as f:
            file = {"patterns": {"episode": ep_pattern,
                                 "batch": batch_pattern,
                                 "movie": movie_pattern}}
            save_json(f, file)

    def get_sources(self) -> sources_type:
         return self.SOURCES
            
    # def getEpisodeNumber(self, filename:str) -> tuple[int,int]:
    #     return TMDB_manipulator().bestMatchTV(filename)

