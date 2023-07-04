from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional
from typing import Type

import requests
from bs4 import BeautifulSoup


class CommonParser(ABC):
    BASE_URL = "https://mydramalist.com"

    def element_parser(
        self,
        elements: List[BeautifulSoup],
        query: str,
        offset: int = 2,
        type: Optional[Type[Any]] = None,
    ) -> Optional[str]:
        for element in elements:
            if query in element.text:
                text = element.text.strip()
                text = text[text.find(":") + offset :]
                if type:
                    text = type(text)
                return text
        return None

    def scrape(self, query: str) -> bool:
        query = self.process_query(query)
        r = requests.get(self.BASE_URL + "/" + query)
        if r.status_code == 404:
            return False
        self.soup = BeautifulSoup(r.content, "html.parser")
        return True

    @abstractmethod
    def process_query(self, query: str) -> str:
        pass

    @abstractmethod
    def parse_model(self) -> Any:
        pass
