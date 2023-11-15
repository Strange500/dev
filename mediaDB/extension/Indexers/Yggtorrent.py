from os.path import isfile
import requests as r
import bs4
from typing import Dict
import feedparser
from urllib.parse import urlparse, parse_qs


from mediaDB.extension.Indexers.common import IndexerCommon
from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.exceptions import *
from mediaDB.flaresolver import *

class Yggtorrent_manipulator():
        
        PASS_KEY: str|None
        TIMEOUT: int|None
        cloudflared: bool|None
        domain: str|None
        rss_movie: str|None
        rss_tv: str|None
        show_episode_search_engine_url: str|None
        show_batch_search_engine_url: str|None
        movie_search_engine_url: str|None
        anime_episode_search_engine_url: str|None
        anime_batch_search_engine_url: str|None
        anime_movie_search_engine_url: str|None
    # CONST
        NAME = "YggTorrent"
        CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/YggTorrent"
        SETTING_FILE = os.path.join(IndexerCommon.SETTING_DIRECTORY, NAME)
        VAR_DIRECTORY = os.path.join(IndexerCommon.VAR_DIRECTORY, NAME)
        CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
        CACHE_DB_TV_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv.json")
        CACHE_DB_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, "DB_movie.json")
        media_types = [1, 3]

        # CREATE NEEDED FILES & DIRECTORY
        os.makedirs(VAR_DIRECTORY, exist_ok=True)
        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
                # Download TMDB config file if not created
        if not isfile(SETTING_FILE) and not wget(CONFIG_EXEMPLE_URL, SETTING_FILE):
            raise ProviderConfigError
        if not isfile(CACHE_DB_TV_FILE) :
            with open(CACHE_DB_TV_FILE, "w", encoding="utf-8") as f:
                dump({}, f, indent=5)
        if not isfile(CACHE_DB_MOVIE_FILE) :
            with open(CACHE_DB_MOVIE_FILE, "w", encoding="utf-8") as f:
                dump({}, f, indent=5)

        # VARIABLE

        PASS_KEY = None
        TIMEOUT = None
        cloudflared = None
        domain = None
        rss_movie = None
        rss_tv = None
        show_episode_search_engine_url = None
        show_batch_search_engine_url = None
        movie_search_engine_url = None
        anime_episode_search_engine_url = None
        anime_batch_search_engine_url = None
        anime_movie_search_engine_url = None

        # SETTING UP 
        if not isfile(SETTING_FILE) and not wget(CONFIG_EXEMPLE_URL):
            raise Exception
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            CONFIG = load(f)
        if CONFIG["active"]:
            PASS_KEY = CONFIG["pass_key"]
            TIMEOUT = CONFIG["timeout"]
            cloudflared = CONFIG["cloudflared"]
            domain = CONFIG["domain"]
            if CONFIG["rss_active"]:
                rss_movie = CONFIG["rss_movie"]
                rss_tv = CONFIG["rss_tv"]
            if CONFIG["search_engine_active"]:
                show_episode_search_engine_url = CONFIG["show_episode_search_engine_url"]
                show_batch_search_engine_url = CONFIG["show_batch_search_engine_url"]
                movie_search_engine_url = CONFIG["movie_search_engine_url"]
                anime_episode_search_engine_url = CONFIG["anime_episode_search_engine_url"]
                anime_batch_search_engine_url = CONFIG["anime_batch_search_engine_url"]
                anime_movie_search_engine_url = CONFIG["anime_movie_search_engine_url"]
        
        if cloudflared and domain is not None:
            PROXY = FlareSolverrProxy(domain)
        else:
            PROXY = None

        def __get_dl_link(self, torrent_id:int):
            dl_link = f"{self.domain}/rss/download?id={torrent_id}&passkey={self.PASS_KEY}"
            return dl_link
        
        def __get_feed(self, url) -> feedparser.FeedParserDict|None:
            if self.cloudflared and self.PROXY is not None:
                response = self.PROXY.get(url)
                if response.status_code != 200:
                    return None
                feed = feedparser.parse(response.content)
                return feed
            return None
        
        def __get_feed_info(self, feed: feedparser.FeedParserDict|None) -> Dict[str, int|str]|None:
            if feed is None:
                return None
            result = dict()
            for entry in feed.entries:
                if 'title' in entry and "link" in entry:
                    title = str(entry.title)
                    seeders = title.split(" ").pop().split("L:")[-1][:1]
                    if seeders.isnumeric():
                        seeders = int(seeders)
                    else:
                        seeders = 0

                    link = str([k["href"] for k in entry["links"] if k['rel'] == 'enclosure'][0])
                    print(link)
                    id = int(link.split("rss/download?id=")[1].split("&passkey=")[0])
                    
                    result[title] = {"seeders": seeders,
                                     "torrent_id": id
                                     }
            return result
        
        def fed(self):
            from pprint import pprint
            feed = self.__get_feed('https://www3.yggtorrent.wtf/rss?action=generate&type=subcat&id=2179&passkey=1Jv4VqOP6LpdNJGv2WcWKQ8sHLKMDbM2')
            result = self.__get_feed_info(feed)
            pprint(result)


## reste stocker et normaliser le resultat ! on ne normalise pas le stockage 
                                        ## ! car les link peuvent changer
## reste a scrap les search engine
##    - faire fonction de dl (on normalise a cas ou il y est des choses specifique pour dl ex: cloudflared)
##    - scrap ep puis nfo  





            
            
