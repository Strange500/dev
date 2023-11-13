from mediaDB.common import *
from mediaDB.settings import *


class IndexerCommon():

    # VARIABLES
    SETTING_DIRECTORY = os.path.join(CONF_DIR, "Indexers")
    VAR_DIRECTORY = os.path.join(VAR_DIR, "Indexers")
    PROXY = FlareSolverrProxy

    # CREATING FILES & DIRECTORIES
    os.makedirs(SETTING_DIRECTORY, exist_ok=True)
    os.makedirs(VAR_DIRECTORY, exist_ok=True)

    wanted_nfo_specification = ["format", "codec id", "duration", "width",
                                "height", "language", "resolution", "hauteur", "largeur", "duree"]
    wanted_nfo_title = ["text", "video", "audio", "mkv"]

    def make_result(self, file_title:str, link: str, media_type: int, seed:int|None=None, codec_id_video:str|None = None,
                    duration:int|None=None, height:int|None=None, width:int|None=None,
                         languages:list|None=[], codec_id_audio:str|None=None ) -> dict:
        ...