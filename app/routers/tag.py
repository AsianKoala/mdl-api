from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.drama import Tag

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=List[schemas.TagBase])
async def get_tags(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = None,
):
    query = db.query(Tag)
    if search:
        query = query.filter(Tag.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit).all()
    return query
