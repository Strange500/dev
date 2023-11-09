from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.exceptions import *
from json import load


class mediaType():

    MEDIA_TYPES_FILE = os.path.join(CONF_DIR, "media_types.json")
    MEDIA_TYPES_JSON_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/media_types.json"

    if not os.path.isfile(MEDIA_TYPES_FILE) and not wget(MEDIA_TYPES_JSON_URL, MEDIA_TYPES_FILE):
        raise MediaTypesFilesDoesNotExist
    with open(MEDIA_TYPES_FILE, "r") as f:
        MEDIA_TYPES = load(f)

    def __init__(self, id:int) -> None:
        try:
            data = self.MEDIA_TYPES[f"{id}"]
        except KeyError:
            raise MediaTypeDoesNotExist
        self.__name = data["name"]
        self.__id = id
        self.have_season = data["have_season"]
        self.only_sound = data["only_sound"]
        self.readable = data["readable"]
        

