from datetime import datetime
from typing import List, Optional
from core.log import generate_logger
from db.crud.drama import CRUDDrama

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
import requests
from scrapers.parse import DramaParser
from sqlalchemy.orm import Session
from sqlalchemy.orm.strategy_options import joinedload

from app import schemas
from app.database import get_db
from app.models.drama import Drama, Genre, IDCache, Tag

router = APIRouter(prefix="/dramas", tags=["Dramas"])
crud = CRUDDrama()
logger = generate_logger()

@router.get("/", response_model=List[schemas.Drama])
async def get_dramas(
    db: Session = Depends(get_db),
    genres: List[int] = Query(None),
    limit: int = 10,
    skip: int = 0,
    tags: List[int] = Query(None),
    search: Optional[str] = None
):
    query = (
        db
        .query(Drama)
        .options(joinedload(Drama.genres))
        .filter(genres)
    )
    logger.info("genres: %s", genres)
    if search:
        query = query.filter(Drama.title.ilike(f"%{search}%"))
    query = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )
    return query

@router.get("/{id}", response_model=schemas.Drama)
async def get_drama(id: int, db: Session = Depends(get_db)):
    query = db.query(Drama).filter(Drama.id == id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Drama with id: {id} not found",
        )
    return query

def drama_check_update(db: Session, drama: Drama):
    date = datetime.now()
    update_date = drama.parse_date
    time_delta = date - update_date
    logger.info("Drama %s last update time: %s", drama.id, time_delta.__str__())

    if time_delta.days >= 1:
        logger.info("Reparsing drama (id=%s), ")
        parser = DramaParser()
        parser.scrape(drama.full_id)
        model = parser.parse_model()
        crud.update_drama(db, model.id, model)
    else:
        logger.info("Fresh drama 9} kept")

@router.get("/long/{long_id}", response_model=schemas.Drama)
async def get_longid_drama(long_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    query = db.query(Drama).filter(Drama.full_id == long_id).first()

    if query:
        background_tasks.add_task(drama_check_update, db, query)
        return query

    else:
        parser = DramaParser()
        status = parser.scrape(long_id)
        if status:
            model = parser.parse_model()
            crud.create_drama(db, model)
            logger.info("Created drama (id=%s) on get", long_id)
            db.refresh(model)
            return model
        else:
            logger.error("Drama (id=%s) does not exist", long_id)
            return None

