from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.drama import Genre

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("/", response_model=List[schemas.GenreBase])
def get_genres(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = None,
):
    query = db.query(Genre)
    if search:
        query = query.filter(Genre.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit).all()
    return query
