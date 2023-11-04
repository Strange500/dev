from mediaDB.common import *
from mediaDB.exceptions import *
from json import load

def createMediaType(name:str, have_season:bool | None = False) -> bool:
    if not (isinstance(name, str) and isinstance(have_season, bool)):
        raise ValueError("function createMediaType: argument must have the right type as indicated in function signature")
    data = dict(load(MEDIA_TYPES_FILE, "r"))
    data[next_id(data)] = {"name": name,
                           "have_season": have_season}
    with open(MEDIA_TYPES_FILE, "w") as f:
        dump(data, f)

    return True

def deleteMediaType(id: int) -> bool:
    if not (isinstance(id, int)):
        raise ValueError("function createMediaType: argument must have the right type as indicated in function signature")
    data = dict(load(MEDIA_TYPES_FILE, "r"))
    if data.get(f"{id}", None) is None:
        return False
    data.pop(f"{id}")
    with open(MEDIA_TYPES_FILE, "w") as f:
        dump(data, f)
    return True

class mediaType():

    MEDIA_TYPES_FILE = os.path.join(CONF_DIR, "media_types.json")
    MEDIA_TYPES_JSON_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/media_types.json"

    if not os.path.isfile(MEDIA_TYPES_FILE) and not wget(MEDIA_TYPES_JSON_URL, MEDIA_TYPES_FILE):
        raise MediaTypesFilesDoesNotExist
    with open(MEDIA_TYPES_FILE, "r") as f:
        MEDIA_TYPES = load(f)

    def __init__(self, id:int) -> None:
        data = self.MEDIA_TYPES[f"{self.__id}"]
        self.__name = data["name"]
        self.__id = id
        self.have_season = data["have_season"]
        self.only_sound = data["only_sound"]
        self.readable = data["readable"]
        

