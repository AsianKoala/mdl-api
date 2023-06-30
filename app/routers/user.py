from datetime import datetime
from typing import List, Optional

from core.log import generate_logger
from db.crud.user import CRUDUser
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from scrapers.user import UserParser
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.user import User

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
            crud.create_user(db, model)
            logger.info("Created user (username=%s) on get", username)
            db.refresh(model)
            return model

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User (username={username}) does not exist",
            )


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
    return models


@router.get("/{username}", response_model=schemas.User)
async def get_user(
    background_tasks: BackgroundTasks, username: str, db: Session = Depends(get_db)
) -> Optional[User]:
    model = crud.get_user(db, username)
    return __fetch_user(db, background_tasks, model, username)
