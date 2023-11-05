class MediaNotFoundERROR(Exception):
    "Raise if an indexer can't find a media in it's database"

class MediaTypeNotSupported(Exception):
    "Raise if media type is not supported"

class MediaTypeDoesNotExist(Exception):
    "Raised if the media type is not initialsed"

class ProviderConfigError(Exception):
    "Raised if a config file is not initialised"

class MediaTypesFilesDoesNotExist(Exception):
    "Raised if a config file is not initialised"

class ProviderConfigError(Exception):
    "Raised if a config file is not initialised"

class TMDBError(Exception):
    "Raised if a error occured in tmdb manipulator"

class IdDoesNotExist(TMDBError):
    "Raised if you try to acess an tmdb id that doesn't exist"

class MalformedTMDBInfo(TMDBError):
    "Raised is tmdb_info does not have the required keys"