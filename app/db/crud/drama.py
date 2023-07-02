from typing import Any, Dict, List, Optional, Tuple

from core.log import generate_logger
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.drama import Drama, Genre, Tag

logger = generate_logger()


class CRUDDrama:
    ATTR_UNION = Tag | Genre

    def get_drama_by_id(self, db: Session, id: int) -> Optional[Drama]:
        return db.query(Drama).filter(Drama.id == id).first()

    def get_drama_by_full_id(self, db: Session, full_id: str) -> Optional[Drama]:
        return db.query(Drama).filter(Drama.full_id == full_id).first()

    def get_dramas(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> List[Drama]:
        query = db.query(Drama)
        if search:
            query = query.filter(Drama.title.ilike(f"%{search}%"))
        query = query.offset(offset).limit(limit).all()
        return query

    def __clean_type(
        self, db: Session, model: ATTR_UNION, values: List[ATTR_UNION]
    ) -> Tuple[List[ATTR_UNION], List[bool]]:
        valid_list = []
        add_to_db = []
        for val in values:
            q = db.query(model).filter(model.title == val.title)
            if q.count() != 0:
                valid = q.first()
                add = False
            else:
                valid = val
                add = True
            valid_list.append(valid)
            add_to_db.append(add)
        return valid_list, add_to_db

    def __add_type(self, db: Session, vals: List[ATTR_UNION], add_list: List[bool]):
        for i, add in enumerate(add_list):
            if add:
                db.add(vals[i])
                db.commit()

    def create_drama(self, db: Session, drama: Drama) -> Optional[Drama]:
        # check if drama already exists
        obj = db.query(Drama).filter(Drama.id == drama.id).first()
        if obj:
            logger.error(f"Drama id={drama.id} already exists within database")
            return None

        clean_t, add_t = self.__clean_type(db, Tag, drama.tags)
        clean_g, add_g = self.__clean_type(db, Genre, drama.genres)
        drama.tags = clean_t
        drama.genres = clean_g

        db.add(drama)
        db.commit()

        self.__add_type(db, clean_t, add_t)
        self.__add_type(db, clean_g, add_g)

        logger.info("Created drama (id=%s)", drama.id)

        return drama

    def update_drama(
        self, db: Session, short_id: int, in_data: Drama | Dict[str, Any]
    ) -> Optional[Drama]:
        # verify drama exists within the database
        obj = db.query(Drama).filter(Drama.id == short_id).first()
        if not obj:
            logger.error(f"Drama id={short_id} does not exist within database")
            return None

        data = jsonable_encoder(obj)

        if isinstance(in_data, dict):
            for attr in data:
                if attr in in_data:
                    setattr(obj, attr, in_data[attr])

            db.commit()
            db.refresh(obj)

        # this case only happens when we update the drama from parse
        else:
            self.delete_drama(db, short_id)
            obj = self.create_drama(db, in_data)

        return obj

    def delete_drama(self, db: Session, short_id: int) -> Optional[Drama]:
        obj = db.query(Drama).filter(Drama.id == short_id).first()
        if not obj:
            logger.error(f"Drama id={short_id} not found in the database")
            return None

        db.delete(obj)
        db.commit()
        return obj
