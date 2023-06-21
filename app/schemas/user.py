from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    following: int
    followers: int
    points: int
    last_online: str
    gender: Optional[str]
    location: Optional[str]
    contribution_points: str
    roles: List[str]
    join_date: str
    show_watchtime: Optional[str]
    episodes: Optional[str]
    shows: Optional[str]
    movie_watchtime: Optional[str]
    movies: Optional[str]

    class Config:
        orm_mode = True
