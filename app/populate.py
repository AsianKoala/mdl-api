from typing import List
from sqlalchemy import Boolean, func, literal_column

from sqlalchemy.orm import Session
from app import schemas
from app.database import SessionLocal
from app.models.drama import Drama, DramaTag, Genre, Tag
from app.scrapers.parse import DramaParser
from app.scrapers.scrape import IDScraper, Options
from app.db.base import Base
from routers import genres
import database

one = "35729-emergency-lands-of-love"
two = "49865-psycho-but-it-s-okay"
three = "32925-hotel-del-luna"

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

def add_drama(db: Session,
              drama: Drama,
              genres: List[Genre],
              tags: List[Tag]):
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

def main():
    # delete_data()
    pass
    

if __name__ == "__main__":
    main()
