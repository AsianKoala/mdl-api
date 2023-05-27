from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from typing import List, Optional

from app import schemas
from app.database import get_db
from app.models.drama import Drama

router = APIRouter(prefix='/dramas', tags=['Dramas'])

@router.get('/', response_model=List[schemas.Drama])
async def get_dramas(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = None):
    query = db.query(Drama)
    if search: query = query.filter(Drama.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit).all()
    return query

@router.get('/{id}', response_model=schemas.Drama)
async def get_drama(id: int, db: Session = Depends(get_db)):
    query = db.query(Drama).filter(Drama.short_id == id)
    if query.count() != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Drama with id: {id} not found")
    drama = query.first()
    return drama
