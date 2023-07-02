from typing import List

from pydantic import BaseModel
from schemas.drama import Drama


class Watchlist(BaseModel):
    id: int
    currently_watching: List[Drama]
    completed: List[Drama]
    plan_to_watch: List[Drama]
    on_hold: List[Drama]
    dropped: List[Drama]

    class Config:
        orm_mode = True
