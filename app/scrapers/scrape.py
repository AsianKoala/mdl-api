from typing import Any, Dict, List, Optional, Set, Tuple, Type

import requests
import os
import json
import time
import re
from bs4 import BeautifulSoup

class Options:
    dramas: Optional[str] = "68"
    drama_special: Optional[str] = "83"
    movies: Optional[str] = "77"
    tv_shows: Optional[str] = "86"

    def __init__(
            self, 
            dramas: bool = False,
            drama_special: bool = False,
            movies: bool = False,
            tv_shows: bool = False,
         ):
        if not dramas: self.DRAMAS = None
        if not drama_special: self.DRAMA_SPECIAL = None
        if not movies: self.MOVIES = None
        if not tv_shows: self.TV_SHOWS = None
        self.any: bool = any([dramas, drama_special, movies, tv_shows])

class IDScraper:
    BASE_URL = "https://mydramalist.com"
    START_YEAR = 2000
    END_YEAR = 2023

    def __init__(self, force_refresh_cache: bool = False):
        self.cache_fname = os.path.join("app", ".cache", "id_cache.json")
        if force_refresh_cache:
            self.__create_cache()
        self.id_set = self.__load_cache()
        self.new_items: List[str] = []

    def __create_cache(self) -> Dict[str, List[str]]:
        with open(self.cache_fname, 'w') as f:
            cache_json = {'data': []}
            json.dump(cache_json, f)
            return cache_json

    def __load_cache(self) -> Set[str]:
        try:
            os.utime(self.cache_fname, None)
            with open(self.cache_fname, 'r') as f:
                cache = json.load(f)
        except OSError:
            cache = self.__create_cache()

        s: Set[str] = set()
        for id in cache['data']:
            s.add(id)

        return s

    def __extract_year_query(self, url: str) -> str:
        pattern = "re=\d+,(\d+)\&"
        p = re.compile(pattern)
        m = re.search(p, url)
        return m.group(1)

    def __build_search_url(
            self,
            end_year: str,
            page: str,
            opts: Options
        ) -> str:
        url = self.BASE_URL + "/search?adv=titles&"
        if opts.any:
            url += "ty="
            if opts.dramas: url += opts.dramas + ","
            if opts.drama_special: url += opts.drama_special + ","
            if opts.movies: url += opts.movies + ","
            if opts.tv_shows: url += opts.tv_shows + ","
            url += "&"
        url += f"re=1890,{end_year}&so=newest&or=desc&page={page}"
        return url

    def write_cache(self):
        cache = {}
        with open(self.cache_fname, 'r') as f:
            cache = json.load(f)

        for id in self.new_items:
            cache['data'].append(id)

        with open(self.cache_fname, 'w') as f:
            json.dump(cache, f)

    def crawl(
            self,
            opts: Options,
            sleep_sec: float = 1.0,
        ) -> List[List[str]]:
        result = []
        for year in range(self.START_YEAR, self.END_YEAR + 1):
            year_ids = self.scrape_year_ids(year, opts, sleep_sec=sleep_sec)
            result.append(year_ids)
        return result

    def scrape_year_ids(
            self,
            year: int,
            opts: Options,
            page_start: int = 1,
            page_end: int = 250,
            sleep_sec: float = 1.0,
        ) -> List[str]:
        if page_start < 1 or page_end > 250:
            raise ValueError("Pages must be in bounds [1,250]")

        all_ids = []
        for page in range(page_start, page_end + 1):
            time.sleep(sleep_sec)
            url = self.__build_search_url(year, page, opts)
            ids = self.parse_page(url)
            if not ids:
                print("[crawler] Skipping page", page)
                continue

            print("[parser] Parsed page", page)
            for id in ids:
                all_ids.append(id)

        print("[crawler] Finished crawling")
        return all_ids

    def parse_page(self, url: str) -> Optional[List[str]]:
        year_q = self.__extract_year_query(url)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        path = os.path.join('.cache', 'test.html')
        with open(path, 'w') as f:
            f.write(soup.prettify())
        link_elements = soup.find_all("a", attrs={"class": "block"})
        year_elements = soup.find_all("span", attrs={"class": "text-muted"})

        ids = []
        for element in link_elements:
            id = element['href'][1:]
            if id not in self.id_set:
                ids.append(id)
                self.new_items.append(id)

        for element in year_elements:
            desc: str = element.text
            idx = desc.index('-')
            year = desc[idx + 2:idx + 6]

            if year != year_q:
                return None

        return ids


