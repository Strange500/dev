from common import *
from exceptions import *
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


    def __init__(self, id:int) -> None:
        data = dict(load(MEDIA_TYPES_FILE))
        if data.get(f"{self.__id}", None) is None:
            raise MediaTypeDoesNotExist
        data = data[f"{self.__id}"]
        self.__name = data["name"]
        self.__id = id
        self.have_season = data["have_season"]

    def delete(self) -> bool:
        data = dict(load(MEDIA_TYPES_FILE))
        if data.get(f"{self.__id}", None) is None:
            return False
        deleteMediaType(self.__id)
        return True

