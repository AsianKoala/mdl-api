from typing import List

from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.cast import Actor
from app.models.cast import Cinematographer
from app.models.cast import Composer
from app.models.cast import Director
from app.models.cast import Screenwriter


class DramaGenre(Base):
    __tablename__ = "drama_genre"

    drama_id = Column(Integer, ForeignKey("drama.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)


class DramaTag(Base):
    __tablename__ = "drama_tag"

    drama_id = Column(Integer, ForeignKey("drama.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)


class Drama(Base):
    __tablename__ = "drama"

    id = Column(Integer, primary_key=True)
    parse_date = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
    full_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    ratings = Column(Integer, nullable=True)
    watchers = Column(Integer, nullable=True)
    reviews = Column(Integer, nullable=True)
    native_title = Column(String, nullable=True)
    known_as = Column(ARRAY(String), nullable=True)
    screenwriter = Column(String, nullable=True)
    director = Column(String, nullable=True)
    country = Column(String, nullable=True)
    episodes = Column(Integer, nullable=True)
    aired = Column(String, nullable=True)
    aired_on = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    original_network = Column(String, nullable=True)
    content_rating = Column(String, nullable=True)
    ranked = Column(Integer, nullable=True)
    popularity = Column(Integer, nullable=True)

    genres = relationship("Genre", secondary="drama_genre", back_populates="dramas")
    tags = relationship("Tag", secondary="drama_tag", back_populates="dramas")

    directors: Mapped[List["Director"]] = relationship(
        secondary="director_drama", back_populates="dramas"
    )
    screenwriters: Mapped[List["Screenwriter"]] = relationship(
        secondary="screenwriter_drama", back_populates="dramas"
    )
    actors: Mapped[List["Actor"]] = relationship(
        secondary="actor_drama", back_populates="dramas"
    )
    composers: Mapped[List["Composer"]] = relationship(
        secondary="composer_drama", back_populates="dramas"
    )
    cinematographers: Mapped[List["Cinematographer"]] = relationship(
        secondary="cinematographer_drama", back_populates="dramas"
    )


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    dramas = relationship("Drama", secondary="drama_genre", back_populates="genres")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    dramas = relationship("Drama", secondary="drama_tag", back_populates="tags")


class IDCache(Base):
    __tablename__ = "idcache"

    id = Column(Integer, primary_key=True, unique=True)
    long_id = Column(String, nullable=False)
