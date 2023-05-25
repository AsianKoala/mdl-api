from datetime import datetime
from typing import List
from pydantic import BaseModel

class DramaBase(BaseModel):
    short_id: str
    full_id: str
    title: str
    year: str
    type: str
    description: str
    rating: float
    num_ratings: str
    watchers: int
    native_title: str
    known_as: List[str]
    screenwriter: str
    country: str
    start_date: datetime
    end_date: datetime
    duration_m: datetime
    aired_on: datetime
    original_network: List[str]
    content_rating: str
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
