from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserDrama(Base):
    __tablename__ = "user_dramas"
    drama_id = Column(ForeignKey("dramas.id"), primary_key=True)
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    status = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    following = Column(Integer, nullable=False)
    followers = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    last_online = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    contribution_points = Column(String, nullable=False)
    roles = Column(String, nullable=False)
    join_date = Column(String, nullable=False)
    show_watchtime = Column(String, nullable=True)
    episodes = Column(Integer, nullable=True)
    shows = Column(Integer, nullable=True)
    movie_watchtime = Column(String, nullable=True)
    movies = Column(Integer, nullable=True)

    watchlist = relationship("Drama", secondary="user_drama", back_populates="users")

