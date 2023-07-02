from pydantic import BaseModel


class GenreBase(BaseModel):
    id: int = None
    title: str

    class Config:
        orm_mode = True
