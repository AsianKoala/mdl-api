from typing import List, Optional, Tuple

from bs4 import BeautifulSoup
from models.drama import Drama
from sqlalchemy.orm import Session
from app.models.user import User
from app.scrapers.common import CommonParser

class UserParser(CommonParser):
    def process_query(self, query: str) -> str:
        self.user = query
        link = "profile/" + query
        return link

    def parse_model(self) -> User:
        episodes, shows = self.parse_episodes_shows()

        last_online, gender, location, contribution_points, roles, join_date = self.parse_details()

        model_dict = {
            "username": self.user,
            "following": self.parse_following(),
            "followers": self.parse_followers(),
            "points": self.parse_points(),
            "last_online": last_online,
            "gender": gender,
            "location": location,
            "contribution_points": contribution_points,
            "roles": roles,
            "join_date": join_date,
            "show_watchtime": self.parse_show_watchtime(),
            "movie_watchtime": self.parse_movie_watchtime(),
            "episodes": episodes,
            "shows": shows,
            "movie_watchtime": self.parse_movie_watchtime(),
            "movies": self.parse_movies()
        }

        user = User(**model_dict)
        return user

    def parse_following(self) -> str:
        element = self.soup.find("div", attrs={"class":"stats-following"})
        following = int(element.find("span").text)
        return following

    def parse_followers(self) -> str:
        element = self.soup.find("div", attrs={"class":"stats-followers"})
        followers = int(element.find("span").text)
        return followers

    def parse_points(self) -> str:
        element = self.soup.find("div", attrs={"class":"stats-points"})
        points = int(element.find("span").text)
        return points

    def parse_details(self) -> Tuple[Optional[str]]:
        elements = self.soup.find_all("li", attrs={"class": "list-item p-a-0"})
        return (
            self.parse_last_online(elements),
            self.parse_gender(elements),
            self.parse_location(elements),
            self.parse_contribution_points(elements),
            self.parse_roles(elements),
            self.parse_join_date(elements)
        )

    def parse_last_online(self, elements: List[BeautifulSoup]) -> str:
        return self.element_parser(elements, "Last Online")

    def parse_gender(self, elements: List[BeautifulSoup]) -> Optional[str]:
        try:
            return self.element_parser(elements, "Gender")
        except:
            return None

    def parse_location(self, elements: List[BeautifulSoup]) -> Optional[str]:
        try:
            return self.element_parser(elements, "Location")
        except:
            return None

    def parse_contribution_points(self, elements: List[BeautifulSoup]) -> str:
        return self.element_parser(elements, "Contribution Points")

    def parse_roles(self, elements: List[BeautifulSoup]) -> List[str]:
        return self.element_parser(elements, "Roles").split(" ")

    def parse_join_date(self, elements: List[BeautifulSoup]) -> str:
        return self.element_parser(elements, "Join Date")

    def parse_show_watchtime(self) -> Optional[str]:
        try:
            element = self.soup.find("div", attrs={"class":"col-sm-6xb-r"})
            return element.text.strip().splitlines()[0]
        except:
            return None

    def parse_episodes_shows(self) -> Optional[List[str]]:
        try:
            element = self.soup.find("div", attrs={"class":"col-sm-6xb-r"})
            data = element.text.strip().splitlines()
            stats_raw = data[-1].split(" ")
            stats_raw = [stats_raw[0], stats_raw[2]]
            return [int(x.replace(",", "")) for x in stats_raw] 
        except:
            return None

    def parse_movie_watchtime(self) -> Optional[str]:
        try:
            element = self.soup.find("div", attrs={"class":"col-sm-6x b-t"""})
            data = element.text.strip().splitlines()
            return data[0]
        except:
            return None

    def parse_movies(self) -> Optional[str]:
        try:
            element = self.soup.find("div", attrs={"class":"col-sm-6x b-t"""})
            data = element.text.strip().splitlines()
            return int(data[-1].split(" ")[0].replace(",", ""))
        except:
            return None

