from sqlalchemy import ARRAY, TIMESTAMP, UUID, Boolean, Column, Date, Float, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship

import uuid

from app.models.base import Base

movie_genre_association_table = Table(
        "movie_genres",
        Base.metadata,
        Column('drama_id', ForeignKey('dramas.id'), primary_key=True),
        Column('genre_id', ForeignKey('genres.id'), primary_key=True)
)

movie_tag_association_table = Table(
        "movie_tags",
        Base.metadata,
        Column('drama_id', ForeignKey('dramas.id'), primary_key=True),
        Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

class Drama(Base):
    __tablename__ = 'dramas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_id = Column(String, nullable=False)
    full_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    num_ratings = Column(Integer, nullable=False)
    watchers = Column(Integer, nullable=False)
    native_title = Column(String, nullable=True)
    known_as = Column(ARRAY(String), nullable=True)
    screenwriter = Column(String, nullable=True)
    director = Column(String, nullable=True)
    country = Column(String, nullable=False)
    episodes = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    duration_m = Column(Integer, nullable=True)
    aired_on = Column(String, nullable=True)
    original_network = Column(ARRAY(String), nullable=True)
    content_rating = Column(String, nullable=True)
    ranked = Column(Integer, nullable=False)
    popularity = Column(Integer, nullable=False)

    genres = relationship(
            secondary=movie_genre_association_table,
            back_populates='dramas'
        )

    tags = relationship(
            secondary=movie_genre_association_table,
            back_populates='dramas'
        )

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    dramas = relationship(
            secondary=movie_genre_association_table,
            back_populates='genres'
    )

class Tags(Base):
    __tablename__ = 'tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    dramas = relationship(
            secondary=movie_genre_association_table,
            back_populates='tags'
    )


