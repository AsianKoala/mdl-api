from typing import Dict, List, Optional, Set, Tuple

import requests
import os
import json
import time
import re
from bs4 import BeautifulSoup

class IDScraper:
    BASE_URL = "https://mydramalist.com"
    START_YEAR = 2000
    END_YEAR = 2023
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

    def __init__(self, force_refresh_cache: bool = False):
        self.cache_fname = os.path.join(".", "id_cache.json")
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

    def __extract_year_query(self, url: str) -> str:
        pattern = "re=\d+,(\d+)\&"
        p = re.compile(pattern)
        m = re.search(p, url)
        return m.group(1)

    def parse_page(self, url: str) -> Optional[List[str]]:
        year_q = self.__extract_year_query(url)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        with open('test.html', 'w') as f:
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

class DramaParser:
    BASE_URL = "https://mydramalist.com"

    def __init__(self, long_ids: List[str]):
        self.ids = long_ids

    def scrape(self, id: str) -> BeautifulSoup:
        r = requests.get(self.BASE_URL + "/" + id)
        soup = BeautifulSoup(r.content, "html.parser")
        self.parse_schema(id, soup)
        return soup

    def parse_schema(self, id: str, soup: BeautifulSoup):
        short_id = id[:id.find('-')]
        long_id = id
        title, year = self.parse_title_year(soup)
        type = 'Drama'
        description = self.parse_description(soup)
        rating, ratings, watchers, reviews = self.parse_user_info(soup)
        native_title = self.parse_native_title(soup)
        known_as = self.parse_known_as(soup)
        screenwriter = self.parse_screenwriter(soup)
        director = self.parse_director(soup)
        country, type, episodes, aired, aired_on, original_network, duration, ranked, popularity, content_rating = self.parse_infotable(soup)
        genres = self.parse_genres(soup)
        tags = self.parse_tags(soup)

    def parse_title_year(self, soup: BeautifulSoup) -> Tuple[str, str]:
        pattern = r"(.+) \((\d+)\) -"
        p = re.compile(pattern)
        title = soup.find("title").text
        m = re.search(p, title)
        return (m.group(1), m.group(2))

    def parse_description(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            synopsis = soup.find('div', attrs={'class':'show-synopsis'})
            descr = synopsis.p.span.text
            return descr
        except:
            return None

    def parse_user_info(self, soup: BeautifulSoup) -> Tuple:
        elements = soup.find_all('div', attrs={'class':'hfs'})
        all_text = ""
        for element in elements: all_text += element.text.strip()
        pattern = r".*: (.*)\/.* from (.*) users.*: (.*)Reviews: (.*) users"
        p = re.compile(pattern)
        m = re.search(p, all_text)

        def clean_str(s): return s.replace(',', '')

        return float(m.group(1)), int(clean_str(m.group(2))), int(clean_str(m.group(3))), int(clean_str(m.group(4)))

    def __element_parser(self, elements: List[BeautifulSoup], query: str, colon: bool = True) -> Optional[str]:
        for element in elements:
            if query in element.text:
                text = element.text.strip()
                if colon:
                    return text[text.find(':')+2:]
                return text
        return None

    def parse_native_title(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            elements = soup.find_all('li', attrs={'class':'list-item p-a-0'})
            return self.__element_parser(elements, "Native Title")
        except:
            return None

    def parse_known_as(self, soup: BeautifulSoup) -> Optional[List[str]]:
        try:
            aka_titles = soup.find('span', attrs={'class':'mdl-aka-titles'})
            children = aka_titles.findChildren('a', recursive=False)
            return list(map(lambda x: x.text, children))
        except:
            return None

    def parse_screenwriter(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            elements = soup.find_all('li', attrs={'class':'list-item p-a-0'})
            return self.__element_parser(elements, "Screenwriter")
        except:
            return None

    def parse_director(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            elements = soup.find_all('li', attrs={'class':'list-item p-a-0'})
            return self.__element_parser(elements, "Director")
        except:
            return None

    def parse_infotable(self, soup: BeautifulSoup) -> Tuple:
        infotable = soup.find('ul', attrs={'class':'list m-a-0 hidden-md-up'})
        infotable_elements = infotable.find_all('li', attrs={'class':'list-item p-a-0'})

        country = self.__element_parser(infotable_elements, 'Country')
        type = self.__element_parser(infotable_elements, 'Drama')
        episodes = self.__element_parser(infotable_elements, 'Episodes')
        aired = self.__element_parser(infotable_elements, 'Aired')
        aired_on = self.__element_parser(infotable_elements, 'Aired On')
        original_network = self.__element_parser(infotable_elements, 'Original Network')
        duration = self.__element_parser(infotable_elements, 'Duration')
        ranked = self.__element_parser(infotable_elements, 'Ranked')
        popularity = self.__element_parser(infotable_elements, 'Popularity')
        content_rating = self.__element_parser(infotable_elements, 'Content Rating')

        return country, type, episodes, aired, aired_on, original_network, duration, ranked, popularity, content_rating

    def parse_genres(self, soup: BeautifulSoup) -> Optional[List[str]]:
        try:
            genres = soup.find('li', attrs={'class':'list-item p-a-0 show-genres'}).find_all('a')
            return list(map(lambda x: x.text.strip(), genres))
        except:
            return None


    def parse_tags(self, soup: BeautifulSoup) -> Optional[List[str]]:
        try:
            tags = soup.find('li', attrs={'class':'list-item p-a-0 show-tags'}).find_all('a', attrs={'class':'text-primary'})
            return list(map(lambda x: x.text.strip(), tags))
        except:
            return None




