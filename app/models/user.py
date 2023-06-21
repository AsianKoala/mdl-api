from sqlalchemy import ARRAY, Column, DateTime, Integer, String, func

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parse_date = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
    username = Column(String, nullable=False)
    following = Column(Integer, nullable=False)
    followers = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    last_online = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    contribution_points = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)
    join_date = Column(String, nullable=False)
    show_watchtime = Column(String, nullable=True)
    episodes = Column(Integer, nullable=True)
    shows = Column(Integer, nullable=True)
    movie_watchtime = Column(String, nullable=True)
    movies = Column(Integer, nullable=True)
