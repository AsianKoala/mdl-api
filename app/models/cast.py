from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DirectorDrama(Base):
    __tablename__ = "director_drama"

    director_id: Mapped[int] = mapped_column(
        ForeignKey("director.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class ScreenwriterDrama(Base):
    __tablename__ = "screenwriter_drama"

    screenwriter_id: Mapped[int] = mapped_column(
        ForeignKey("screenwriter.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class ActorDrama(Base):
    __tablename__ = "actor_drama"

    actor_id: Mapped[int] = mapped_column(ForeignKey("actor.id"), primary_key=True)
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class ComposerDrama(Base):
    __tablename__ = "composer_drama"

    composer_id: Mapped[int] = mapped_column(
        ForeignKey("composer.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class CinematographerDrama(Base):
    __tablename__ = "cinematographer_drama"

    cinematographer_id: Mapped[int] = mapped_column(
        ForeignKey("cinematographer.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class Director(Base):
    __tablename__ = "director"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_id: Mapped[str]
    name: Mapped[str]
    dramas: Mapped[List["Drama"]] = relationship(secondary="director_drama", back_populates="directors")  # type: ignore


class Screenwriter(Base):
    __tablename__ = "screenwriter"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_id: Mapped[str]
    name: Mapped[str]
    dramas: Mapped[List["Drama"]] = relationship(secondary="screenwriter_drama", back_populates="screenwriters")  # type: ignore


class Actor(Base):
    __tablename__ = "actor"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_id: Mapped[str]
    name: Mapped[str]
    dramas: Mapped[List["Drama"]] = relationship(secondary="actor_drama", back_populates="actors")  # type: ignore


class Composer(Base):
    __tablename__ = "composer"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_id: Mapped[str]
    name: Mapped[str]
    dramas: Mapped[List["Drama"]] = relationship(secondary="composer_drama", back_populates="composers")  # type: ignore


class Cinematographer(Base):
    __tablename__ = "cinematographer"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_id: Mapped[str]
    name: Mapped[str]
    dramas: Mapped[List["Drama"]] = relationship(secondary="cinematographer_drama", back_populates="cinematographers")  # type: ignore
