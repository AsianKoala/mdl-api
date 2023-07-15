import re
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type

import requests
from bs4 import BeautifulSoup
from core.log import generate_logger
from scrapers.common import CommonParser
from sqlalchemy.orm import Session

from app.models.drama import Drama
from app.models.drama import Genre
from app.models.drama import Tag
from app.models.cast import Actor
from app.models.cast import Cinematographer
from app.models.cast import Composer
from app.models.cast import Director
from app.models.cast import Screenwriter

logger = generate_logger()


class DramaParser(CommonParser):
    def process_query(self, query: str) -> str:
        self.id = query
        return query

    def parse_model(self, db: Session) -> Drama:
        id = self.id[: self.id.find("-")]
        full_id = self.id
        title, year = self.parse_title_year()
        description = self.parse_description()
        rating, ratings, watchers, reviews = self.parse_user_info()
        native_title = self.parse_native_title()
        known_as = self.parse_known_as()
        screenwriter = self.parse_screenwriter()
        director = self.parse_director()
        (
            country,
            type,
            episodes,
            aired,
            aired_on,
            release_date,
            original_network,
            duration,
            ranked,
            popularity,
            content_rating,
        ) = self.parse_infotable()
        genres = self.parse_genres()
        tags = self.parse_tags()

        # change soup for cast download
        r = requests.get(f"{self.BASE_URL}/{full_id}/cast")
        self.soup = BeautifulSoup(r.content, "html.parser")

        genres = [Genre(title=x) for x in genres]
        tags = [Tag(title=x) for x in tags]

        model_dict = {
            "id": id,
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

        return drama

    def parse_title_year(self) -> Tuple[str, str]:
        pattern = r"(.+) \((\d+)\) -"
        p = re.compile(pattern)
        title = self.soup.find("title").text
        m = re.search(p, title)
        return (m.group(1), int(m.group(2)))

    def parse_description(self) -> Optional[str]:
        try:
            synopsis = self.soup.find("div", attrs={"class": "show-synopsis"})
            descr = synopsis.p.span.text
            return descr
        except:
            return None

    def parse_user_info(self) -> Tuple:
        try:
            elements = self.soup.find_all("div", attrs={"class": "hfs"})
            all_text = ""
            for element in elements:
                all_text += element.text.strip()
            pattern = r".*: (.*)\/.* from (.*) users.*: (.*)Reviews: (.*) users"
            p = re.compile(pattern)
            m = re.search(p, all_text)

            def clean_str(s):
                return s.replace(",", "")

            def safe_cast(a, b):
                try:
                    return a(b)
                except:
                    return None

            return (
                safe_cast(float, m.group(1)),
                safe_cast(int, clean_str(m.group(2))),
                safe_cast(int, clean_str(m.group(3))),
                safe_cast(int, clean_str(m.group(4))),
            )
        except:
            return (None, None, None, None)

    def parse_native_title(self) -> Optional[str]:
        try:
            elements = self.soup.find_all("li", attrs={"class": "list-item p-a-0"})
            return self.element_parser(elements, "Native Title")
        except:
            return None

    def parse_known_as(self) -> Optional[List[str]]:
        try:
            aka_titles = self.soup.find("span", attrs={"class": "mdl-aka-titles"})
            children = aka_titles.findChildren("a", recursive=False)
            return list(map(lambda x: x.text, children))
        except:
            return None

    def parse_screenwriter(self) -> Optional[str]:
        try:
            elements = self.soup.find_all("li", attrs={"class": "list-item p-a-0"})
            return self.element_parser(elements, "Screenwriter")
        except:
            return None

    def parse_director(self) -> Optional[str]:
        try:
            elements = self.soup.find_all("li", attrs={"class": "list-item p-a-0"})
            return self.element_parser(elements, "Director")
        except:
            return None

    def parse_infotable(self) -> Tuple:
        infotable = self.soup.find("ul", attrs={"class": "list m-a-0 hidden-md-up"})
        infotable_elements = infotable.find_all(
            "li", attrs={"class": "list-item p-a-0"}
        )

        country = self.element_parser(infotable_elements, "Country")
        type = self.element_parser(infotable_elements, "Type")
        episodes = self.element_parser(infotable_elements, "Episodes", type=int)
        aired = self.element_parser(infotable_elements, "Aired")
        aired_on = self.element_parser(infotable_elements, "Aired On")
        release_date = self.element_parser(infotable_elements, "Release Date")
        original_network = self.element_parser(infotable_elements, "Original Network")
        duration = self.element_parser(infotable_elements, "Duration")
        ranked = self.element_parser(infotable_elements, "Ranked", offset=3, type=int)
        popularity = self.element_parser(
            infotable_elements, "Popularity", offset=3, type=int
        )
        content_rating = self.element_parser(infotable_elements, "Content Rating")

        return (
            country,
            type,
            episodes,
            aired,
            aired_on,
            release_date,
            original_network,
            duration,
            ranked,
            popularity,
            content_rating,
        )

    def parse_genres(self) -> Optional[List[str]]:
        try:
            genres = self.soup.find(
                "li", attrs={"class": "list-item p-a-0 show-genres"}
            ).find_all("a")
            return list(map(lambda x: x.text.strip(), genres))
        except:
            return None

    def parse_tags(self) -> Optional[List[str]]:
        try:
            tags = self.soup.find(
                "li", attrs={"class": "list-item p-a-0 show-tags"}
            ).find_all("a", attrs={"class": "text-primary"})
            return list(map(lambda x: x.text.strip(), tags))
        except:
            return None

    def parse_cast():
        pass

    def parse_directors(self, db: Session) -> List[Director]:
        # remove after done testing
        r = requests.get("https://mydramalist.com/35729-emergency-lands-of-love/cast")
        soup = BeautifulSoup(r.content, "html.parser")
        # end remove

        directors = []
        elements = soup.find_all("h3", attrs={"class":"header b-b p-b"})



        print(elements[2])

        person_class = "col-xs-3 col-sm-4 p-r p-l-0"

        print(soup.find_all("h3", attrs={"class":"header b-b p-b"})[1].next.next.next.find("a", attrs={"class":"text-primary text-ellipsis"})['href'])

        return directors
