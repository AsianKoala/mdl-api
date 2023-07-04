from datetime import datetime
from typing import List
from typing import Optional

from core.log import generate_logger
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from scrapers.user import UserParser
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.db.crud.user import CRUDUser
from app.models.user import User
from app.models.watchlist import Watchlist
from app.scrapers.watchlist import WatchlistParser

router = APIRouter(prefix="/users", tags=["Users"])
crud = CRUDUser()
logger = generate_logger()


def __check_update(db: Session, user: User):
    date = datetime.now()
    update_date = user.parse_date.replace(tzinfo=date.tzinfo)
    time_delta = date - update_date
    logger.info(
        "User (username=%s) delta update time: %s", user.username, time_delta.__str__()
    )

    if time_delta.days >= 1:
        logger.info("Reparsing user (username=%s)", user.username)
        parser = UserParser()
        parser.scrape(user.username)
        model = parser.parse_model()
        crud.update_user(db, model.username, model)
    else:
        logger.info("Not reparsing user (username=%s)", user.username)


def __fetch_user(
    db: Session, background_tasks: BackgroundTasks, model: Optional[User], username: str
) -> Optional[User]:
    if model:
        background_tasks.add_task(__check_update, db, model)
        return model

    else:
        parser = UserParser()
        is_success = parser.scrape(username)

        if is_success:
            model = parser.parse_model()
            if model:
                crud.create_user(db, model)
                logger.info("Created user (username=%s) on get", username)
                db.refresh(model)
                return model

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User (username={username}) does not exist",
        )


def __download_watchlist(db: Session, model: User):
    db_watchlist = db.query(Watchlist).filter(Watchlist.id == model.id).first()

    # check parse date
    days = 0
    if db_watchlist:
        date = datetime.now()
        update_date = db_watchlist.parse_date.replace(tzinfo=date.tzinfo)
        time_delta = date - update_date
        logger.info(
            "Watchlist (username=%s) delta update time: %s",
            model.username,
            time_delta.__str__(),
        )
        days = time_delta.days

    if not db_watchlist or days >= 1:
        parser = WatchlistParser()
        parser.scrape(model.username)
        watchlist = parser.parse_model(db)

        # simply just add to db
        if not db_watchlist:
            logger.info("Downloaded watchlist for user (username=%s)", model.username)
            db.add(watchlist)
            db.commit()

        else:
            logger.info("Updating watchlist for user (username=%s)", model.username)
            update_data = jsonable_encoder(watchlist)
            old_data = jsonable_encoder(db_watchlist)

            for attr in old_data:
                if attr in update_data:
                    setattr(db_watchlist, attr, update_data[attr])

            db_watchlist.parse_date = datetime.now()

            db.commit()
            db.refresh(db_watchlist)

        db_watchlist = watchlist

    return db_watchlist


@router.get("/", response_model=List[schemas.User])
async def get_users(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> List[User]:
    models = crud.get_users(db, offset=offset, limit=limit, search=search)
    for model in models:
        background_tasks.add_task(__check_update, db, model)
        background_tasks.add_task(__download_watchlist, db, model)
    return models


@router.get("/{username}", response_model=schemas.User)
async def get_user(
    background_tasks: BackgroundTasks, username: str, db: Session = Depends(get_db)
) -> Optional[User]:
    cached_obj = crud.get_user(db, username)
    model = __fetch_user(db, background_tasks, cached_obj, username)
    background_tasks.add_task(__download_watchlist, db, model)
    return model


@router.get("/{username}/watchlist", response_model=schemas.Watchlist)
async def get_watchlist(
    background_tasks: BackgroundTasks, username: str, db: Session = Depends(get_db)
) -> Optional[Watchlist]:
    cached_obj = crud.get_user(db, username)
    user_model = __fetch_user(db, background_tasks, cached_obj, username)
    return __download_watchlist(db, user_model)
