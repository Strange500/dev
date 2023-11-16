from os.path import isfile
import requests as r
from bs4 import BeautifulSoup
from typing import Dict
import feedparser
from urllib.parse import urlparse, parse_qs
from thefuzz import fuzz
import time


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
        CACHE_DB_TV_BATCH_FILE:str
        CACHE_DB_TV_BATCH:Dict[str, Dict[str, int]]
        CACHE_DB_MOVIE_FILE:str
        CACHE_DB_MOVIE:Dict[str, Dict[str, int]]
        CACHE_DB_TV_FILE:str
        CACHE_DB_TV:Dict[str, Dict[str, int]]
    # CONST
        NAME = "YggTorrent"
        CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/YggTorrent"
        SETTING_FILE = os.path.join(IndexerCommon.SETTING_DIRECTORY, NAME)
        VAR_DIRECTORY = os.path.join(IndexerCommon.VAR_DIRECTORY, NAME)
        CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
        CACHE_DB_TV_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv.json")
        CACHE_DB_TV_BATCH_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv.json")
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
        if not isfile(CACHE_DB_TV_BATCH_FILE) :
            with open(CACHE_DB_TV_BATCH_FILE, "w", encoding="utf-8") as f:
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
        wanted_nfo_specification = None
        wanted_nfo_title = None
        nbSecBetweenReq = None

        # SETTING UP 
        if not isfile(SETTING_FILE) and not wget(CONFIG_EXEMPLE_URL, SETTING_FILE):
            raise Exception
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            CONFIG = load(f)
        if CONFIG["active"]:
            PASS_KEY = CONFIG["pass_key"]
            TIMEOUT = CONFIG["timeout"]
            cloudflared = CONFIG["cloudflared"]
            domain = CONFIG["domain"]
            wanted_nfo_specification = CONFIG["wanted_nfo_specification"]
            wanted_nfo_title = CONFIG["wanted_nfo_title"]
            nbSecBetweenReq = CONFIG["nbSecBetweenReq"]
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

        with open(CACHE_DB_TV_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_TV = load(f)
        with open(CACHE_DB_TV_BATCH_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_TV_BATCH = load(f)
        with open(CACHE_DB_MOVIE_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_MOVIE = load(f)

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
        
        def __store_results_tv(self, results: Dict[str, Dict[str, int]]) -> None:
            if isinstance(results, dict):
                self.CACHE_DB_TV = {**self.CACHE_DB_TV , **results}
                with open(self.CACHE_DB_TV_FILE) as f:
                    save_json(f, self.CACHE_DB_TV)
        def __store_results_tv_batch(self, results: Dict[str, Dict[str, int]]) -> None:
            if isinstance(results, dict):
                self.CACHE_DB_TV_BATCH = {**self.CACHE_DB_TV_BATCH , **results}
                with open(self.CACHE_DB_TV_BATCH_FILE) as f:
                    save_json(f, self.CACHE_DB_TV_BATCH)

        def __store_results_movie(self, results: Dict[str, Dict[str, int]]) -> None:
            if isinstance(results, dict):
                self.CACHE_DB_MOVIE = {**self.CACHE_DB_MOVIE , **results}
                with open(self.CACHE_DB_MOVIE_FILE) as f:
                    save_json(f, self.CACHE_DB_MOVIE)

        def __parse_page(self, url:str) -> tuple[dict | None, int | None] | None:

            def extract_text_from_tr(html):
                matching_trs = html.find_all('tr')
                results = []
                list_trs = []
                for tr in matching_trs:
                    for td in tr.find_all("td"):
                        if td.find("a", {"id": "torrent_name"}) is not None:
                            list_trs.append(tr)
                for tr in list_trs:
                    tds = tr.find_all('td')
                    before_last_td = tds[-2]
                    text = before_last_td.get_text(strip=True)
                    results.append(text)
                return results
            
            if self.PROXY is None:
                return
            response = self.PROXY.get(url)
            html = BeautifulSoup(response.content, features="html.parser")
            ## processing html
            h2_tags_with_font = [h2_tag for h2_tag in html.find_all("h2") if h2_tag.find("font", style="float: right")]
            if len(h2_tags_with_font) == 0:
                return None, None
            text_contents = [font_tag.text.strip() for h2_tag in h2_tags_with_font for font_tag in
                            h2_tag.find_all("font")]
            ##
            total_result = int(text_contents[0].split(" ")[0])
            target_elements = html.find_all("a", id="get_nfo")
            target_values = [element["target"] for element in target_elements]
            torrent_name_elements = html.find_all("a", id="torrent_name")
            torrent_names = [element.text.strip() for element in torrent_name_elements]
            seeders = extract_text_from_tr(html)
            return {f"{name}": {"id": id, "seeders": seed} for name, id, seed in
                    zip(torrent_names, target_values, seeders)}, total_result
                
        def __get_next_page_url(self, url_base: str, n_total_item: int):
            if not len([i for i in url_base.split("&") if "page=" in i]) > 0:
                n_item = 0
                url_base = url_base + f"&page={n_item}"
            else:
                n_item = int([i for i in url_base.split("&") if "page=" in i][0].split("=")[-1])
            if n_item > n_total_item:
                return None
            else:
                n_url = url_base.replace(f"page={n_item}", f"page={n_item + 50}")
                return n_url
            
        def __get_value_nfo(self, part: str) -> tuple[str, str]:
            """funtion specific to nfo files that have key values style separed by ':'"""
            key, value = "", ""
            while part != "" and part[0] != ":":
                key += part[0]
                part = part[1:]
            part, key = part[1:], key.replace(".", "").lower().strip()
            while part != "":
                value += part[0]
                part = part[1:]
            value = value.strip()
            return (key, value)
        
        def __prepare_nfo(self, nfo_content: str):
            content = bytes(str(nfo_content).replace('b"<pre>', "").replace('\n</pre>"', ""), "utf-8").decode(
                'unicode_escape', errors='ignore')
            content, result = content.split("\n"), {}
            temp, title, result = {}, None, []
            for lines in content:
                temp = ""
                for car in lines:
                    if (car.isalnum() or car == " " or car == "." or car == ":") and car != "â":
                        temp += car
                result.append(temp.strip())
            return result
        
        def __get_nfo(self, id_torrent: int) -> dict|None:
            if self.PROXY is None:
                return
            url = f'{self.domain}/engine/get_nfo?torrent={id_torrent}'
            if not validators.url(url):
                return
            response = self.PROXY.get(f'{self.domain}/engine/get_nfo?torrent={id_torrent}')
            content, result = self.__prepare_nfo(str(response)), {}
            temp, title = {}, None
            for part in content:
                key, value = self.__get_value_nfo(part)
                if key == "" and value == "":
                    continue
                elif key != "" and value == "":
                    if title is not None:
                        if temp != {title: {}}:
                            result = {**result, **deepcopy(temp)}
                        temp.clear()
                    key = self.__wanted_title_nfo(key)
                    if key:
                        title = key
                        temp[title] = {}
                    else:
                        key = "None"
                if title is not None and title != key and len(str(key)) < 30 and len(value) < 60 and key != "None":
                    key = self.__wanted_spe_nfo(str(key))
                    if temp.get(title, None) is None:
                        temp[title] = {}
                    if key:
                        temp[title][key] = value
            result = {**result, **deepcopy(temp)}
            return delete_empty_dictionnaries(result)
        
        def __wanted_title_nfo(self, key: str) -> str | bool:
            if self.wanted_nfo_title is None:
                return False
            key = remove_non_ascii(key).lower()
            for wanted in self.wanted_nfo_title:
                wanted_ori = wanted
                wanted = remove_non_ascii(wanted).lower()
                if fuzz.ratio(key, wanted) > 65:
                    return wanted_ori
            return False
        
        def __wanted_spe_nfo(self, key: str) -> str | bool:
            if self.wanted_nfo_specification is None:
                return False
            key = remove_non_ascii(key).lower()
            for wanted in self.wanted_nfo_specification:
                wanted_ori = wanted
                wanted = remove_non_ascii(wanted).lower()
                if fuzz.ratio(key, wanted) > 80:
                    return wanted_ori
            return False
        
        def get_results(self, url: str, title: str): # on en est la 
            results = {}
            title = title.replace(" ", "+")
            url = url.replace("< search >", title)
            item, n_tot = self.__parse_page(url)
            if item is None:
                return None
            results = {**results, **item}
            time.sleep(1)
            url = self.__get_next_page_url(url, n_tot)
            while url is not None:
                item, temp = self.parse_page(url)
                if item is not None:
                    results = {**results, **item}
                time.sleep(1)
                url = self.get_next_page_url(url, n_tot)
            return results
        
        def get_ep(self, titles:list[str], season: int, episode: int, is_show=False, is_anime=False):
            if is_show and self.show_episode_search_engine_url is not None:
                list_source = [self.show_episode_search_engine_url]
            elif is_anime and self.anime_episode_search_engine_url is not None:
                list_source = [self.anime_episode_search_engine_url]
            else:
                list_source = [i for i in [self.anime_episode_search_engine_url, self.show_episode_search_engine_url] if i is not None]
            
            results =  dict()
            for url in list_source:
                results = {**results, **self.__ge}
        
        def fed(self):
            from pprint import pprint
            feed = self.__get_feed('https://www3.yggtorrent.wtf/rss?action=generate&type=subcat&id=2179&passkey=1Jv4VqOP6LpdNJGv2WcWKQ8sHLKMDbM2')
            result = self.__get_feed_info(feed)
            pprint(result)

Yggtorrent_manipulator().fed()
## reste stocker et normaliser le resultat ! on ne normalise pas le stockage 
                                        ## ! car les link peuvent changer
## reste a scrap les search engine
##    - faire fonction de dl (on normalise a cas ou il y est des choses specifique pour dl ex: cloudflared)
##    - scrap ep puis nfo  





            
            
