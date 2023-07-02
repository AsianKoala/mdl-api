from typing import Optional

from core.log import generate_logger
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.crud.drama import CRUDDrama
from app.models.user import User
from app.models.watchlist import Watchlist
from app.routers.drama import update_idcache
from app.scrapers.common import CommonParser
from app.scrapers.parse import DramaParser

logger = generate_logger()


class WatchlistParser(CommonParser):
    def process_query(self, query: str) -> str:
        self.user = query.strip()
        link = "dramalist/" + query
        return link

    def __get_cls(self, num) -> str:
        return f"mdl-style-list mdl-style-list-{num} box"

    def __parse_list(self, db: Session, cls: str) -> Optional[Watchlist]:
        crud = CRUDDrama()
        drama_parser = DramaParser()

        soup = self.soup.find("div", attrs={"class": cls}).find("tbody")
        dramas = soup.find_all("td", attrs={"class": "mdl-style-col-title sort1"})

        drama_list = []

        for drama in dramas:
            full_id = drama.a["href"][1:]
            model = crud.get_drama_by_full_id(db, full_id)
            if not model:
                scraper_status = drama_parser.scrape(full_id)

                if not scraper_status:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Drama (id={full_id}) not found",
                    )

                model = drama_parser.parse_model()

                update_idcache(db, model)
                crud.create_drama(db, model)

            drama_list.append(model)

        return drama_list

    def parse_model(self, db: Session) -> Optional[Watchlist]:
        try:
            user_id = db.query(User).filter(User.username == self.user).first().id

            lists = []
            for i in range(1, 6):
                drama_list = self.__parse_list(db, self.__get_cls(i))
                lists.append(drama_list)

            model_dict = {"id": user_id}

            watchlist = Watchlist(**model_dict)
            watchlist.currently_watching = lists[0]
            watchlist.completed = lists[1]
            watchlist.plan_to_watch = lists[2]
            watchlist.on_hold = lists[3]
            watchlist.dropped = lists[4]

            return watchlist

        except:
            logger.error("Watchlist failed to parse")
