from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class DramaBase(BaseModel):
    short_id: str
    full_id: str
    title: str
    year: str
    type: str
    description: Optional[str]
    rating: float
    ratings: int
    watchers: int
    reviews: int
    native_title: Optional[str]
    known_as: Optional[List[str]]
    screenwriter: Optional[str]
    director: Optional[str]
    country: str
    episodes: Optional[int]
    aired: Optional[str]
    aired_on: Optional[str]
    release_date: Optional[str]
    duration: Optional[str]
    original_network: Optional[str]
    content_rating: Optional[str]
    ranked: int
    popularity: int

    class Config:
        orm_mode = True

class GenreBase(BaseModel):
    title: str

class Genre(BaseModel):
    dramas: List[DramaBase]

class TagBase(BaseModel):
    title: str

class Tag(TagBase):
    dramas: List[DramaBase]

class Drama(DramaBase):
    genres: List[GenreBase]
    tags: List[TagBase]
