from datetime import datetime, timedelta
from typing import List, Optional
from core.log import generate_logger
from db.crud.drama import CRUDDrama

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
import requests
from scrapers.parse import DramaParser
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.orm.strategy_options import joinedload

from app import schemas
from app.database import get_db
from app.models.drama import Drama, Genre, IDCache, Tag

router = APIRouter(prefix="/dramas", tags=["Dramas"])
crud = CRUDDrama()
logger = generate_logger()

def __check_update(db: Session, drama: Drama):
    date = datetime.now()
    update_date = drama.parse_date.replace(tzinfo=date.tzinfo)
    time_delta = date - update_date
    logger.info("Drama (id=%s) delta update time: %s", drama.id, time_delta.__str__())

    if time_delta.days >= 1:
        logger.info("Reparsing drama (id=%s)", drama.id)
        parser = DramaParser()
        parser.scrape(drama.full_id)
        model = parser.parse_model()
        crud.update_drama(db, model.id, model)
    else:
        logger.info("Not reparsing drama (id=%s)", drama.id)

def __fetch_drama(model: Optional[Drama], long_id: str, background_tasks: BackgroundTasks, db: Session) -> Optional[Drama]:
    if model:
        background_tasks.add_task(__check_update, db, model)
        return model

    else:
        parser = DramaParser()
        status = parser.scrape(long_id)

        if status:
            model = parser.parse_model()

            # let's also update IDCache if necessary
            id_check = db.query(IDCache).filter(IDCache.long_id == long_id).first()
            if not id_check:
                db.add(IDCache(id=model.id, long_id=long_id))
                db.commit()

            crud.create_drama(db, model)
            logger.info("Created drama (id=%s) on get", long_id)
            db.refresh(model)
            return model
        else:
            logger.error("Drama (id=%s) does not exist", long_id)
            return None

def build_sql(genre_ids: Optional[List[int]], tag_ids: Optional[List[int]], search: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> str:
    select = "SELECT dramas.* FROM dramas"
    if limit: limit_sql = "LIMIT {} ".format(limit)
    else: limit_sql = "LIMIT ALL"
    if offset: offset_sql = "OFFSET " + str(offset)
    else: offset_sql = "OFFSET 0"

    def __join_sql(x: str, ids: List[int]) -> str:
        first = (
            """
            LEFT JOIN drama_{} 
            ON dramas.id = drama_{}.drama_id AND drama_{}.{}_id IN ({})
            """
            .format(*([x]*4), ''.join(['{}, ']*(len(ids)-1)) + str(ids[len(ids)-1]))
            .format(*ids)
        )

        second = (
            """
            LEFT JOIN {}s
            ON drama_{}.{}_id = {}s.id
            GROUP BY dramas.id
            HAVING COUNT(DISTINCT {}s.title) = {}
            """
            .format(*([x]*6), len(ids))
        )

        return first + second

    if genre_ids: genre_sql = __join_sql('genre', genre_ids)
    else: genre_sql = ''
    if tag_ids: tag_sql = __join_sql('tag', tag_ids)
    else: tag_sql = ''

    sql = select + genre_sql + tag_sql + limit_sql + offset_sql
    return sql



@router.get("/", response_model=List[schemas.Drama])
async def get_dramas(
    db: Session = Depends(get_db),
    genres: List[int] = Query(None),
    tags: List[int] = Query(None),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = None
) -> List[Drama]:
    sql = text(build_sql(genres, tags, limit, skip))
    rows = db.execute(sql)
    models = [Drama(**r._asdict()) for r in rows]
    return models


@router.get("/{id}", response_model=schemas.Drama)
async def get_drama(id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    long_id = db.query(IDCache).filter(IDCache.id == id).first()
    model = db.query(Drama).filter(Drama.id == id).first()
    return __fetch_drama(model, long_id, background_tasks, db)


@router.get("/long/{long_id}", response_model=schemas.Drama)
async def get_longid_drama(long_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    model = db.query(Drama).filter(Drama.full_id == long_id).first()
    return __fetch_drama(model, background_tasks, db)

