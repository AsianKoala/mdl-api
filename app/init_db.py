from typing import List

from sqlalchemy.orm import Session
from app import schemas
from app.database import SessionLocal
from app.models.drama import Drama, Genre, Tag
from app.scrapers.parse import DramaParser
from app.scrapers.scrape import IDScraper, Options

def add_drama(db: Session, drama: Drama):
    if db.query(Drama).filter(Drama.short_id == drama.short_id).count() == 0:
        db.add(drama)
        db.commit()

def add_genres(db: Session, genres: List[Genre]):
    for genre in genres:
        query = db.query(Genre.title == genre.title)
        if query.count() != 0:
            # update the genre list
            db_genre = query.first()
            new_genre = schemas.Genre(title=genre.title, *db_genre.dramas)
            query.update(new_genre.dict(), synchronize_session=False)
        else:
            # just add
            db.add(genre)

        db.commit()

def add_tags(db: Session, tags: List[Tag]):
    for tag in tags:
        query = db.query(tag.title == tag.title)
        if query.count() != 0:
            # update the tag list
            db_tag = query.first()
            new_tag = schemas.Tag(title=tag.title, *db_tag.dramas)
            query.update(new_tag.dict(), synchronize_session=False)
        else:
            # just add
            db.add(tag)

        db.commit()

def scrape_ids(year: int):
    scraper = IDScraper(force_refresh_cache=False)
    opts = Options(dramas=True)
    ids = scraper.scrape_year_ids(year=year, opts=opts, page_end=2)
    return ids

def scrape_single():
    return ["35729-emergency-lands-of-love"]

def scrape_second_test():
    return ["32925-hotel-del-luna"]

def init_test_data():
    db = SessionLocal()
    parser = DramaParser()

    # ids = scrape_ids(2023)
    # ids = scrape_single()
    ids = scrape_second_test()

    for id in ids:
        parser.scrape(id)
        drama, genres, tags = parser.parse_models()
        add_drama(db, drama)
        add_genres(db, genres)
        add_tags(db, tags)

def test_db_data():
    db = SessionLocal()
    d = db.query(Tag).first()
    s = schemas.Tag.from_orm(d)
    print(s.json())

def main():
    init_test_data()
    # test_db_data()

if __name__ == "__main__":
    main()
