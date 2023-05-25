from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from typing import List, Optional

from app import schemas
from app.database import get_db
from app.models.drama import Drama

router = APIRouter(prefix='/dramas', tags=['Dramas'])

@router.get('/', response_model=List[schemas.Drama])
async def get_dramas(
        db: Session = Depends(get_db),
        limit: int = 10,
        search: str = ""
    ):
    posts = db.query(Drama).filter(Drama.title.ilike(f"%{search}"))
    return posts.first()
