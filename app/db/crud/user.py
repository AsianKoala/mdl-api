from typing import Any, Dict, List, Optional

from core.log import generate_logger
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.user import User

logger = generate_logger()


class CRUDUser:
    def get_user(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username)

    def get_users(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> List[User]:
        query = db.query(User)
        if search:
            query = query.filter(User.username.ilike(f"%{search}%"))
        query = query.offset(offset).limit(limit).all()
        return query

    def create_user(self, db: Session, user: User) -> Optional[User]:
        # check if drama already exists
        obj = db.query(User).filter(User.id == user.id).first()
        if obj:
            logger.error(f"User id={user.id} already exists within database")
            return None

        db.add(user)
        db.commit()

        return user

    def update_user(
        self, db: Session, username: str, in_data: User | Dict[str, Any]
    ) -> Optional[User]:
        # verify drama exists within the database
        obj = db.query(User).filter(User.username == username).first()
        if not obj:
            logger.error(f"User username={username} does not exist within the database")
            return None

        data = jsonable_encoder(obj)

        if isinstance(in_data, dict):
            update_data = in_data
        else:
            update_data = jsonable_encoder(in_data)

        for attr in data:
            if attr in update_data:
                setattr(obj, attr, update_data[attr])

        db.commit()
        db.refresh(obj)

        return obj

    def delete_user(self, db: Session, username: str) -> Optional[User]:
        # verify drama exists within the database
        obj = db.query(User).filter(User.username == username).first()
        if not obj:
            logger.error(f"User username={username} does not exist within the database")
            return None

        db.delete(obj)
        db.commit()
        return obj
