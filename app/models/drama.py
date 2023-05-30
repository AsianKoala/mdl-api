from sqlalchemy import ARRAY, TIMESTAMP, UUID, Boolean, Column, Date, Float, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship

import uuid

from app.db.base_class import Base

class DramaGenre(Base):
    __tablename__ = 'drama_genre'

    drama_id = Column(UUID(as_uuid=True), ForeignKey('dramas.id'), primary_key=True)
    genre_id = Column(UUID(as_uuid=True), ForeignKey('genres.id'), primary_key=True)

class DramaTag(Base):
    __tablename__ = 'drama_tag'

    drama_id = Column(UUID(as_uuid=True), ForeignKey('dramas.id'), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)

class Drama(Base):
    __tablename__ = 'dramas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_id = Column(Integer, nullable=False, unique=True)
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

    genres = relationship("Genre", secondary="drama_genre", back_populates='drama')
    tags = relationship("Tag", secondary="drama_tag", back_populates='drama')

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    drama = relationship("Drama", secondary="drama_genre", back_populates='genres')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    drama = relationship("Drama", secondary="drama_tag", back_populates='tags')

