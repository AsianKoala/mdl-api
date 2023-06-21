from datetime import datetime
from typing import List, Optional

from core.log import generate_logger
from db.crud.user import CRUDUser
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from models.user import User
from scrapers.user import UserParser
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])
crud = CRUDUser()
logger = generate_logger()

def __check_update(db: Session, user: User):
    date = datetime.now()
    update_date = user.parse_date.replace(tzinfo=date.tzinfo)
    time_delta = date - update_date
    logger.info("User (username=%s) delta update time: %s", user.username, time_delta.__str__)

    if time_delta.days >= 1:
        logger.info("Reparsing user (username=%s)", user.username)
        parser = UserParser()
        parser.scrape(user.username)
        model = parser.parse_model()
        crud.update_user(db, model.username, model)
    else:
        logger.info("Not reparsing user (username=%s)", user.username)

@router.get("/", response_model=List[schemas.User])
async def get_users(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[User]:
    return crud.get_users(db, offset=offset, limit=limit, search=search)

@router.get("/{username}", response_model=schemas.User)
async def get_user(username: str, db: Session = Depends(get_db)) -> Optional[User]:
    return crud.get_user(db, username)

