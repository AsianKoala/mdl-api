from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.drama import Drama


class CurrentlyWatching(Base):
    __tablename__ = "currently_watching"

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlist.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class Completed(Base):
    __tablename__ = "completed"

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlist.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class PlanToWatch(Base):
    __tablename__ = "plan_to_watch"

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlist.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class OnHold(Base):
    __tablename__ = "on_hold"

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlist.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class Dropped(Base):
    __tablename__ = "dropped"

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlist.id"), primary_key=True
    )
    drama_id: Mapped[int] = mapped_column(ForeignKey("drama.id"), primary_key=True)


class Watchlist(Base):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    parse_date = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    currently_watching: Mapped[List["Drama"]] = relationship(
        secondary="currently_watching"
    )
    completed: Mapped[List["Drama"]] = relationship(secondary="completed")
    plan_to_watch: Mapped[List["Drama"]] = relationship(secondary="plan_to_watch")
    on_hold: Mapped[List["Drama"]] = relationship(secondary="on_hold")
    dropped: Mapped[List["Drama"]] = relationship(secondary="dropped")
