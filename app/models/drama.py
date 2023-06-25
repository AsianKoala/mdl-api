import enum
from sqlalchemy import ARRAY, Column, DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class DramaGenre(Base):
    __tablename__ = "drama_genre"

    drama_id = Column(Integer, ForeignKey("drama.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)


class DramaTag(Base):
    __tablename__ = "drama_tag"

    drama_id = Column(Integer, ForeignKey("drama.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)


class WatchlistType(enum.Enum):
    currently_watching = 1
    completed = 2
    plan_to_watch = 3
    on_hold = 4
    dropped = 5


class DramaUser(Base):
    __tablename__ = "drama_user"
    drama_id = Column(Integer, ForeignKey("drama.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    status = Column(Enum(WatchlistType))
    drama = relationship("Drama", back_populates="users")
    user = relationship("User", back_populates="dramas")


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

    users = relationship("DramaUser", back_populates="drama")


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


