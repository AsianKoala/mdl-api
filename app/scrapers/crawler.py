import re
import time
from typing import Optional

from bs4 import BeautifulSoup
from core.log import generate_logger
from core.util import retry_request
from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from app.models.drama import IDCache

logger = generate_logger()


class CrawlerOptions:
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
        sleep_time: float = 1.0,
        default_retry_time: float = 60.0,
        max_retries: int = 10,
    ):
        self.sleep_time = sleep_time
        self.default_retry_time = default_retry_time
        self.max_retries = max_retries
        any_params: bool = any([dramas, drama_special, movies, tv_shows])

        url = ""
        if any_params:
            url += "ty="
            if dramas:
                url += self.dramas + ","
            if drama_special:
                url += self.drama_special + ","
            if movies:
                url += self.movies + ","
            if tv_shows:
                url += self.tv_shows + ","
            url += "&"

        self.param_url = url


class IDCrawler:
    BASE_URL = "https://mydramalist.com"
    START_YEAR = 2000
    END_YEAR = 2024

    def __init__(self, db: Session, opts: CrawlerOptions):
        self.db = db
        self.opts = opts
        self.new_ids = []

    # Extract year from search URL
    def __extract_year_query(self, url: str) -> str:
        pattern = "re=\d+,(\d+)\&"
        p = re.compile(pattern)
        m = re.search(p, url)
        return m.group(1)

    # Build search URL
    def __build_search_url(self, end_year: str, page: str) -> str:
        url = self.BASE_URL + "/search?adv=titles&"
        url += self.opts.param_url
        url += f"re=1890,{end_year}&so=newest&or=desc&page={page}"
        return url

    # Crawl a year of ids
    def crawl_year(self, year: int, page_start: int = 1, page_end: int = 250):
        if page_start < 1 or page_end > 250:
            raise ValueError("Pages must be in bounds [1,250]")

        for page in range(page_start, page_end + 1):
            time.sleep(self.opts.sleep_time)

            url = self.__build_search_url(year, page)
            try:
                scraped = self.parse_page(url)
            except:
                logger.error("Error during parsing page %s", page)
                scraped = False

            if not scraped:
                logger.info("Finished crawling at page: %s", page)
                logger.info("Skipping %s pages", page_end - page)
                return

            logger.info("Parsed page: %s", page)

        logger.info("Finished crawling year: %s", year)

    # Returns newly scraped ids
    def parse_page(self, url: str) -> Boolean:
        year_q = self.__extract_year_query(url)

        # r = requests.get(url)
        r = retry_request(
            url, self.opts.default_retry_time, self.opts.max_retries, logger
        )

        soup = BeautifulSoup(r.content, "html.parser")
        link_elements = soup.find_all("a", attrs={"class": "block"})
        year_elements = soup.find_all("span", attrs={"class": "text-muted"})

        all_wrong_year = True
        for element in year_elements:
            desc: str = element.text
            idx = desc.index("-")
            year = desc[idx + 2 : idx + 6]

            if year == year_q:
                all_wrong_year = False

        if all_wrong_year:
            return False

        for element in link_elements:
            long_id = element["href"][1:]
            id = int(long_id[: long_id.find("-")])

            query = self.db.query(IDCache.id).filter(IDCache.id == id)
            exists = self.db.query(query.exists()).scalar()
            if not exists:
                self.new_ids.append((id, long_id))

        return True

    def write_db(self):
        models = map(lambda x: IDCache(id=x[0], long_id=x[1]), self.new_ids)
        self.db.add_all(models)
        self.db.commit()
