from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class DramaBase(BaseModel):
    short_id: int
    full_id: str
    title: str
    year: int
    type: str
    description: Optional[str] = None
    rating: float
    ratings: int
    watchers: int
    reviews: int
    native_title: Optional[str] = None
    known_as: Optional[List[str]] = None
    screenwriter: Optional[str] = None
    director: Optional[str] = None
    country: str
    episodes: Optional[int] = None
    aired: Optional[str] = None
    aired_on: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[str] = None
    original_network: Optional[str] = None
    content_rating: Optional[str] = None
    ranked: int
    popularity: int

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    title: str

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    title: str

    class Config:
        orm_mode = True

class Genre(BaseModel):
    dramas: List[DramaBase]

class Tag(TagBase):
    dramas: List[DramaBase]

class Drama(DramaBase):
    genres: List[GenreBase]
    tags: List[TagBase]

