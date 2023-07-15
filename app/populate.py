from typing import List

import database
import requests
from routers.drama import build_sql
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.log import generate_logger
from app.database import SessionLocal
from app.db.base import Base
from app.db.crud.drama import CRUDDrama
from app.models.drama import Drama
from app.models.drama import Genre
from app.models.drama import Tag
from app.scrapers.crawler import CrawlerOptions
from app.scrapers.crawler import IDCrawler
from app.scrapers.drama import DramaParser

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


def test_sql():
    db = SessionLocal()
    genre_ids = [2]
    # q = db.query(Drama.id).filter(Drama.genres.any(Genre.id.in_(genre_ids))).all()
    first = """
        SELECT dramas.* FROM dramas
        LEFT JOIN drama_genre 
        ON dramas.id = drama_genre.drama_id AND drama_genre.genre_id IN ({})""".format(
        "".join(["{}, "] * (len(genre_ids) - 1)) + str(genre_ids[len(genre_ids) - 1])
    ).format(
        *genre_ids
    )

    second = """
        LEFT JOIN genres
        ON drama_genre.genre_id = genres.id
        GROUP BY dramas.id
        HAVING COUNT(DISTINCT genres.title) = {}""".format(
        len(genre_ids)
    )

    sql = text(first + second)
    rows = db.execute(sql)
    [Drama(**r._asdict()) for r in rows]


def test_build_sql():
    genre_ids = [1, 2]
    tag_ids = [3, 4]
    limit = ""
    offset = ""
    sql = build_sql(genre_ids=genre_ids, tag_ids=tag_ids, limit=limit, offset=offset)
    print(sql)


def main():
    # populate_id_cache()
    # test_logger()
    # init_data()
    # test_404()
    # delete_data()
    # test_sql()
    # test_build_sql()
    test_update()


if __name__ == "__main__":
    main()
