from typing import Dict


from mediaDB.common import *
from mediaDB.settings import *
dict_pattern_type = Dict[str, list[str]] |None
source_type = Dict[str, dict_pattern_type|str]|None
sources_type = Dict[str, source_type|None]|None
class ParserCommon():

    result = {
        "title": str,
        "season": int,
        "episode": int,
        "year": int
    }

    SETTING_DIRECTORY = os.path.join(CONF_DIR, "Parser")
    CACHE_DIRECTORY = os.path.join(VAR_DIR, "Parser")
    

    os.makedirs(SETTING_DIRECTORY, exist_ok=True)
    os.makedirs(CACHE_DIRECTORY, exist_ok=True)


    def normalizeFileName(filename:str):
        result = filename
        filename = replaceDots(filename)
        filename = replaceUnderscore(filename)
        return filename
    
    