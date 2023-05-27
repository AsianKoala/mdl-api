from typing import Any, Dict, List, Optional, Set, Tuple, Type

import requests
import os
import re
from bs4 import BeautifulSoup

from app.models.drama import Drama, Genre, Tag

class DramaParser:
    BASE_URL = "https://mydramalist.com"

    def __element_parser(
            self,
            elements: List[BeautifulSoup],
            query: str,
            offset: int = 2,
            type: Optional[Type[Any]] = None) -> Optional[str]:
        for element in elements:
            if query in element.text:
                text = element.text.strip()
                text = text[text.find(':')+offset:]
                if type:
                    text = type(text)
                return text
        return None

    def scrape(self, id: str):
        self.id = id
        r = requests.get(self.BASE_URL + "/" + id)

        self.soup = BeautifulSoup(r.content, "html.parser")

        path = os.path.join('app', '.cache', 'drama.html')
        with open(path, 'w') as f:
            f.write(self.soup.prettify())

    def parse_models(self) -> Tuple[Drama, List[Genre], List[Tag]]:
        short_id = self.id[:self.id.find('-')]
        full_id = self.id
        title, year = self.parse_title_year()
        description = self.parse_description()
        rating, ratings, watchers, reviews = self.parse_user_info()
        native_title = self.parse_native_title()
        known_as = self.parse_known_as()
        screenwriter = self.parse_screenwriter()
        director = self.parse_director()
        country, type, episodes, aired, aired_on, release_date, original_network, duration, ranked, popularity, content_rating = self.parse_infotable()
        genres = self.parse_genres()
        tags = self.parse_tags()

        genres = [Genre(title=x) for x in genres]
        tags = [Tag(title=x) for x in tags]

        model_dict = {
                "short_id": short_id,
                "full_id": full_id,
                "title": title,
                "year": year,
                "type": type,
                "description": description,
                "rating": rating,
                "ratings": ratings,
                "watchers": watchers,
                "reviews": reviews,
                "native_title": native_title,
                "known_as": known_as,
                "screenwriter": screenwriter,
                "director": director,
                "country": country,
                "type": type,
                "episodes": episodes,
                "aired": aired,
                "aired_on": aired_on,
                "release_date": release_date,
                "duration": duration,
                "original_network": original_network,
                "content_rating": content_rating,
                "ranked": ranked,
                "popularity": popularity,
        }

        drama = Drama(**model_dict)
        drama.genres = genres
        drama.tags = tags

        return drama, genres, tags


    def parse_title_year(self) -> Tuple[str, str]:
        pattern = r"(.+) \((\d+)\) -"
        p = re.compile(pattern)
        title = self.soup.find("title").text
        m = re.search(p, title)
        return (m.group(1), int(m.group(2)))

    def parse_description(self) -> Optional[str]:
        try:
            synopsis = self.soup.find('div', attrs={'class':'show-synopsis'})
            descr = synopsis.p.span.text
            return descr
        except:
            return None

    def parse_user_info(self) -> Tuple:
        elements = self.soup.find_all('div', attrs={'class':'hfs'})
        all_text = ""
        for element in elements: all_text += element.text.strip()
        pattern = r".*: (.*)\/.* from (.*) users.*: (.*)Reviews: (.*) users"
        p = re.compile(pattern)
        m = re.search(p, all_text)

        def clean_str(s): return s.replace(',', '')

        return float(m.group(1)), int(clean_str(m.group(2))), int(clean_str(m.group(3))), int(clean_str(m.group(4)))


    def parse_native_title(self) -> Optional[str]:
        try:
            elements = self.soup.find_all('li', attrs={'class':'list-item p-a-0'})
            return self.__element_parser(elements, "Native Title")
        except:
            return None

    def parse_known_as(self) -> Optional[List[str]]:
        try:
            aka_titles = self.soup.find('span', attrs={'class':'mdl-aka-titles'})
            children = aka_titles.findChildren('a', recursive=False)
            return list(map(lambda x: x.text, children))
        except:
            return None

    def parse_screenwriter(self) -> Optional[str]:
        try:
            elements = self.soup.find_all('li', attrs={'class':'list-item p-a-0'})
            return self.__element_parser(elements, "Screenwriter")
        except:
            return None

    def parse_director(self) -> Optional[str]:
        try:
            elements = self.soup.find_all('li', attrs={'class':'list-item p-a-0'})
            return self.__element_parser(elements, "Director")
        except:
            return None

    def parse_infotable(self) -> Tuple:
        infotable = self.soup.find('ul', attrs={'class':'list m-a-0 hidden-md-up'})
        infotable_elements = infotable.find_all('li', attrs={'class':'list-item p-a-0'})

        country = self.__element_parser(infotable_elements, 'Country')
        type = self.__element_parser(infotable_elements, 'Type')
        episodes = self.__element_parser(infotable_elements, 'Episodes', type=int)
        aired = self.__element_parser(infotable_elements, 'Aired')
        aired_on = self.__element_parser(infotable_elements, 'Aired On')
        release_date = self.__element_parser(infotable_elements, 'Release Date')
        original_network = self.__element_parser(infotable_elements, 'Original Network')
        duration = self.__element_parser(infotable_elements, 'Duration')
        ranked = self.__element_parser(infotable_elements, 'Ranked', offset=3, type=int)
        popularity = self.__element_parser(infotable_elements, 'Popularity', offset=3, type=int)
        content_rating = self.__element_parser(infotable_elements, 'Content Rating')

        return country, type, episodes, aired, aired_on, release_date, original_network, duration, ranked, popularity, content_rating

    def parse_genres(self) -> Optional[List[str]]:
        try:
            genres = self.soup.find('li', attrs={'class':'list-item p-a-0 show-genres'}).find_all('a')
            return list(map(lambda x: x.text.strip(), genres))
        except:
            return None


    def parse_tags(self) -> Optional[List[str]]:
        try:
            tags = self.soup.find('li', attrs={'class':'list-item p-a-0 show-tags'}).find_all('a', attrs={'class':'text-primary'})
            return list(map(lambda x: x.text.strip(), tags))
        except:
            return None
