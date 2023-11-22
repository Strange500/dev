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
        SEARCH_PATTERN = "< search >"
    # CONST
        NAME = "YggTorrent"
        CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/YggTorrent"
        SETTING_FILE = os.path.join(IndexerCommon.SETTING_DIRECTORY, NAME)
        VAR_DIRECTORY = os.path.join(IndexerCommon.VAR_DIRECTORY, NAME)
        CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
        CACHE_DB_TV_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv.json")
        CACHE_DB_TV_BATCH_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv_batch.json")
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
        wanted_nfo_specification = None
        wanted_nfo_title = None
        nbSecBetweenReq = 1
        category = None
        ep_option = None
        limit_ep = None
        season_option = None
        limit_season = None
        language_option = None
        languages = None
        quality_option = None
        qualities = None


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
                category = CONFIG["category"]
                ep_option = CONFIG["ep_option"]
                limit_ep = CONFIG["limit_ep"]
                season_option = CONFIG["season_option"]
                limit_season = CONFIG["limit_season"]
                language_option = CONFIG["language_option"]
                languages = CONFIG["languages"]
                quality_option = CONFIG["quality_option"]
                qualities = CONFIG["qualities"]


        

        with open(CACHE_DB_TV_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_TV = load(f)
        with open(CACHE_DB_TV_BATCH_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_TV_BATCH = load(f)
        with open(CACHE_DB_MOVIE_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_MOVIE = load(f)

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
        
        def __store_results_tv(self, results: Dict[str, Dict[str, int]]) -> None:
            formated_results = {results[i]["id"]: {"torrent_name": i, "seeders": int(results[i]["seeders"]), "nfo": results[i]["nfo"]} for i in results}
            if isinstance(formated_results, dict) and hasattr(self, "CACHE_DB_TV"):
                self.CACHE_DB_TV = {**self.CACHE_DB_TV , **formated_results} # type: ignore
                with open(self.CACHE_DB_TV_FILE, "w") as f:
                    save_json(f, self.CACHE_DB_TV)

        def __store_results_tv_batch(self, results: Dict[str, Dict[str, int]]) -> None:
            formated_results = {results[i]["id"]: {"torrent_name": i, "seeders": int(results[i]["seeders"]), "nfo": results[i]["nfo"]} for i in results}
            if isinstance(formated_results, dict) and hasattr(self, "CACHE_DB_TV_BATCH"):
                self.CACHE_DB_TV_BATCH = {**self.CACHE_DB_TV_BATCH , **formated_results} # type: ignore
                with open(self.CACHE_DB_TV_BATCH_FILE, "w") as f:
                    save_json(f, self.CACHE_DB_TV_BATCH)

        def __store_results_movie(self, results: Dict[str, Dict[str, int]]) -> None:
            formated_results = {results[i]["id"]: {"torrent_name": i, "seeders": int(results[i]["seeders"]), "nfo": results[i]["nfo"]} for i in results}
            if isinstance(formated_results, dict) and hasattr(self, "CACHE_DB_MOVIE"):
                self.CACHE_DB_MOVIE = {**self.CACHE_DB_MOVIE , **formated_results} # type: ignore
                with open(self.CACHE_DB_MOVIE_FILE, "w") as f:
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
            content, result = self.__prepare_nfo(str(response.content)), {}
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
        
            
        
        def __get_results(self, url: str) -> Dict[str, Dict[str, int]] | None: 
            results = {}
            response = self.__parse_page(url)
            if response is None:
                return None
            item, n_tot = response
            if item is None or n_tot is None:
                return None
            results = {**results, **item}
            time.sleep(self.nbSecBetweenReq)
            n_url = self.__get_next_page_url(url, n_tot)
            while n_url is not None:
                response = self.__parse_page(n_url)
                if response is None:
                    return None
                item, temp = response
                if item is not None:
                    results = {**results, **item}
                time.sleep(1)
                n_url = self.__get_next_page_url(n_url, n_tot)
            for i in results:
                nfo = self.__get_nfo(results[i]["id"])
                if nfo is not None:
                    results[i]["nfo"] = nfo
            return results
        
        # def get_ep(self, titles:list[str], season: int, episode: int, is_show=False, is_anime=False):
        #     if is_show and self.show_episode_search_engine_url is not None:
        #         list_source = [self.show_episode_search_engine_url]
        #     elif is_anime and self.anime_episode_search_engine_url is not None:
        #         list_source = [self.anime_episode_search_engine_url]
        #     else:
        #         list_source = [i for i in [self.anime_episode_search_engine_url, self.show_episode_search_engine_url] if i is not None]
            
        #     results =  dict()
        #     for url in list_source:
        #         results = {**results, **self.__}


        def __make_urls(self, media_type:int, name:str, list_ep:list[int]|str="all", list_season:list[int]|str="all", quality:str|None="all", language:str|str="all", uploader:str="", description:str="", file:str="") -> list[str]|None:
            """make url from search engine"""
            url = f"{self.domain}/engine/search?name={name.replace(' ', '+')}&description={description.replace(' ', '+')}&file={file.replace(' ', '+')}&uploader={uploader}&"
            category = ""
            subcategories = []
            if self.category is None:
                return
            if media_type == 3:
                cat = self.category["film&video"]
                category = cat["id"]
                subcategories = [cat["sub_categories"][i] for i in cat["sub_categories"] if i in ["animation", "animation_serie", "serie_tv"]]
                all_ep = False
                all_season = False
                if list_ep == "all" and self.limit_ep is not None:
                    list_ep = [1]
                    all_ep = True
                if list_season == "all" and self.limit_season is not None:
                        list_season = [1]
                        all_season = True
                if self.ep_option is not None :
                    if not all_ep:
                        for ep in list(list_ep):
                            url += self.ep_option + f"{(int(ep)+1)}" + "&"
                    else:
                        url+= self.ep_option + f"1" + "&"
                if self.season_option is not None :
                    if not all_season:
                        for season in list(list_season):
                            url += self.season_option + f"{(int(season)+3)}" + "&"
                    else:
                        url+= self.season_option + f"1" + "&"
            elif media_type == 1:
                cat = self.category["film&video"]
                category = cat["id"]
                subcategories = [cat["sub_categories"][i] for i in cat["sub_categories"] if i in ["animation", "film"]]

            if self.language_option is not None and self.languages is not None and language != "all" and language in self.languages:  
                url += self.language_option + f"{self.languages[language]}" + "&"
            if self.quality_option is not None and self.qualities is not None and quality != "all" and quality in self.qualities:
                url += self.quality_option + f"{self.qualities[quality]}" + "&"
            
            return [f"{url}category={category}&sub_category={i}&do=search" for i in subcategories]
            
            
        def get_ep(self, titles: list[str]|str, seasons: int|list[int], episodes: int|list[int], tmdb_id: int | None = None) -> Dict[str, Dict[str, int]] | None:
            results = {}
            if isinstance(titles, str):
                titles = [titles]
            if isinstance(episodes, int):
                episodes = [episodes]
            if isinstance(seasons, int):
                seasons = [seasons]
            if len(episodes) < 1:
                return None
            for title in titles:
                print(title)
                urls = self.__make_urls(3, title, list_ep=episodes, list_season=seasons)
                print(urls , "\n")
                if urls is None:
                    return None
                for url in urls:
                    response = self.__get_results(url)
                    if response is not None:
                        results.update(response)
            self.__store_results_tv(results) ##### faire cache correctement
            return results
        
        def get_movie(self, titles: list[str]|str, tmdb_id: int | None = None) -> Dict[str, Dict[str, int]] | None:
            results = {}
            if isinstance(titles, str):
                titles = [titles]
            for title in titles:
                urls = self.__make_urls(1, title)
                if urls is None:
                    return None
                for url in urls:
                    response = self.__get_results(url)
                    if response is not None:
                        results.update(response)
            self.__store_results_movie(results)
            return results
    
        def get_batch(self, titles: list[str]|str, seasons: int|list[int], tmdb_id: int | None = None) -> Dict[str, Dict[str, int]] | None:
            results = {}
            if isinstance(titles, str):
                titles = [titles]
            if isinstance(seasons, int):
                seasons = [seasons]
            for title in titles:
                urls = self.__make_urls(3, title, list_season=seasons)
                if urls is None:
                    return None
                for url in urls:
                    response = self.__get_results(url)
                    if response is not None:
                        results.update(response)
            self.__store_results_tv_batch(results)
            return results
            
                
        
        def download(self, torrent_id: int) -> bytes | None:
            if self.PROXY is None:
                return None
            url = self.__get_dl_link(torrent_id)
            response = self.PROXY.get(url)
            if response.status_code != 200:
                return None
            return response.content
        
        def getTorrentNameAndIdTVEP(self) -> Dict[str, int]:
            return {str(self.CACHE_DB_TV[i]["torrent_name"]): int(i) for i in self.CACHE_DB_TV}
    
        def getTorrentNameAndIdTVBatch(self) -> Dict[str, int]:
            return {str(self.CACHE_DB_TV_BATCH[i]["torrent_name"]): int(i) for i in self.CACHE_DB_TV_BATCH}
        
        def getTorrentNameAndIdMovie(self) -> Dict[str, int]:
            return {str(self.CACHE_DB_MOVIE[i]["torrent_name"]): int(i) for i in self.CACHE_DB_MOVIE}

