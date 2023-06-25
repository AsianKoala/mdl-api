from typing import Any, List, Optional

from pydantic import BaseModel
from pydantic.utils import GetterDict


class GenreBase(BaseModel):
    id: int = None
    title: str

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    id: int = None
    title: str

    class Config:
        orm_mode = True


class DramaBase(BaseModel):
    id: int
    full_id: str
    title: str
    year: int
    type: str
    description: Optional[str] = None
    rating: Optional[float] = None
    ratings: Optional[int] = None
    watchers: Optional[int] = None
    reviews: Optional[int] = None
    native_title: Optional[str] = None
    known_as: Optional[List[str]] = None
    screenwriter: Optional[str] = None
    director: Optional[str] = None
    country: Optional[str] = None
    episodes: Optional[int] = None
    aired: Optional[str] = None
    aired_on: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[str] = None
    original_network: Optional[str] = None
    content_rating: Optional[str] = None
    ranked: Optional[int] = None
    popularity: Optional[int] = None

    class Config:
        orm_mode = True


class UserDramaGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key != "status":
            return getattr(self._obj.drama, key)
        else:
            return super(UserDramaGetter, self).get(key, default)

class UserDramaBase(BaseModel):
    id: int
    full_id: str
    title: str
    year: int
    type: str
    description: Optional[str] = None
    rating: Optional[float] = None
    ratings: Optional[int] = None
    watchers: Optional[int] = None
    reviews: Optional[int] = None
    native_title: Optional[str] = None
    known_as: Optional[List[str]] = None
    screenwriter: Optional[str] = None
    director: Optional[str] = None
    country: Optional[str] = None
    episodes: Optional[int] = None
    aired: Optional[str] = None
    aired_on: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[str] = None
    original_network: Optional[str] = None
    content_rating: Optional[str] = None
    ranked: Optional[int] = None
    popularity: Optional[int] = None

    status: Optional[str] = None

    class Config:
        orm_mode = True
        getter_dict = UserDramaGetter


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

    dramas: List[UserDramaBase]

    class Config:
        orm_mode = True


class Genre(GenreBase):
    dramas: List[DramaBase]


class Tag(TagBase):
    dramas: List[DramaBase]


class Drama(DramaBase):
    genres: List[GenreBase]
    tags: List[TagBase]
