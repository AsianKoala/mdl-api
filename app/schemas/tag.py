from pydantic import BaseModel


class TagBase(BaseModel):
    id: int = None
    title: str

    class Config:
        orm_mode = True
