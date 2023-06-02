from typing import List

import database
import requests
from sqlalchemy.orm import Session

from app.core.log import generate_logger
from app.database import SessionLocal
from app.db.base import Base
from app.db.crud.drama import CRUDDrama
from app.models.drama import Drama, Genre, Tag
from app.scrapers.crawler import CrawlerOptions, IDCrawler
from app.scrapers.parse import DramaParser

one = "35729-emergency-lands-of-love"
two = "49865-psycho-but-it-s-okay"
three = "32925-hotel-del-luna"

logger = generate_logger()


def delete_data():
    Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)


def clean_genres(db: Session, genres: List[Genre]):
    genre_list = []
    add_to_db_list = []
    for genre in genres:
        q = db.query(Genre).filter(Genre.title == genre.title)
        if q.count() != 0:
            valid_g = q.first()
            add_to_db = False
        else:
            valid_g = genre
            add_to_db = True
        genre_list.append(valid_g)
        add_to_db_list.append(add_to_db)
    return genre_list, add_to_db_list


def clean_tags(db: Session, tags: List[Tag]):
    tag_list = []
    add_to_db_list = []
    for tag in tags:
        q = db.query(Tag).filter(Tag.title == tag.title)
        if q.count() != 0:
            valid_g = q.first()
            add_to_db = False
        else:
            valid_g = tag
            add_to_db = True
        tag_list.append(valid_g)
        add_to_db_list.append(add_to_db)
    return tag_list, add_to_db_list


def add_drama(db: Session, drama: Drama, genres: List[Genre], tags: List[Tag]):
    clean_g, add_g = clean_genres(db, genres)
    clean_t, add_t = clean_tags(db, tags)
    drama.genres = clean_g
    drama.tags = clean_t

    db.add(drama)
    db.commit()

    for i, add in enumerate(add_g):
        if add:
            db.add(clean_g[i])
            db.commit()

    for i, add in enumerate(add_t):
        if add:
            db.add(clean_t[i])
            db.commit()


def test_update():
    db = SessionLocal()
    crud = CRUDDrama()
    update_data = {"title": "xd"}
    id = "35729"
    crud.update_drama(db, id, update_data)


def test_delete():
    db = SessionLocal()
    crud = CRUDDrama()
    ids = list(map(lambda x: x[: x.find("-")], [one, two, three]))
    for id in ids:
        crud.delete_drama(db, id)


def init_data():
    db = SessionLocal()
    crud = CRUDDrama()
    parser = DramaParser()
    ids = [one, two, three]
    for id in ids:
        parser.scrape(id)
        drama = parser.parse_model()
        crud.create_drama(db, drama)


def populate_id_cache():
    db = SessionLocal()
    options = CrawlerOptions(dramas=True)
    crawler = IDCrawler(db, options)
    crawler.crawl_year(2020, page_start=1, page_end=2)
    # crawler.write_db()


def test_logger():
    logger.info("test")

def test_404():
    url = "https://mydramalist.com/12345678"
    r = requests.get(url)
    print(r.status_code)

def main():
    # populate_id_cache()
    # test_logger()
    # init_data()
    # test_404()
    delete_data()


if __name__ == "__main__":
    main()
