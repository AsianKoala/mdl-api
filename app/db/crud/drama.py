from typing import Any, Dict, List, Optional, Tuple
from fastapi.encoders import jsonable_encoder
from app.models.drama import Drama, Genre, Tag
import schemas
from sqlalchemy.orm import Session


class CRUDDrama:
    ATTR_UNION = Tag | Genre

    def get_drama_by_title(self, db: Session, title: str) -> Optional[Drama]:
        return db.query(Drama).filter(Drama.title == title).first()

    def get_drama_by_id(self, db: Session, id: int) -> Optional[Drama]:
        return db.query(Drama).filter(Drama.short_id == id).first()

    def get_all_dramas(
            self,
            db: Session,
            offset: int = 0,
            limit: int = 0,
            search: Optional[str] = None
            ) -> List[Drama]:
        query = db.query(Drama)
        if search:
            query = query.filter(Drama.title.ilike(f"%{search}%"))
        query = query.offset(offset).limit(limit).all()
        return query

    def __clean_type(
            self,
            db: Session,
            model: ATTR_UNION,
            values: List[ATTR_UNION]
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

    def __add_type(
            self,
            db: Session,
            vals: List[ATTR_UNION],
            add_list: List[bool]
            ):
        for i, add in enumerate(add_list):
            if add:
                db.add(vals[i])
                db.commit()

    def create_drama(self, db: Session, drama: Drama) -> Drama:
        # check if drama already exists
        schemas.Drama.validate(drama)
        query = db.query(Drama).filter(Drama.title == drama.title)
        if query.count() != 0:
            print(f"Drama {drama.title} already exists within database")
            return None

        clean_t, add_t = self.__clean_type(db, Tag, drama.tags)
        clean_g, add_g = self.__clean_type(db, Genre, drama.genres)
        drama.tags = clean_t
        drama.genres = clean_g

        db.add(drama)
        db.commit()

        self.__add_type(db, clean_t, add_t)
        self.__add_type(db, clean_g, add_g)

        return drama

    def update_drama(
            self,
            db: Session,
            short_id: int,
            in_data: Drama | Dict[str, Any]
            ) -> Optional[Drama]:
        # verify drama exists within the database
        query = db.query(Drama).filter(Drama.short_id == short_id)
        if query.count() == 0:
            print(f"Drama id={short_id} not found in the database")
            return None


        if isinstance(in_data, dict):
            update_data = in_data
        else:
            update_data = in_data.__dict__

        db_obj = query.first()
        data = db_obj.__dict__
        for attr in data:
            if attr in update_data:
                setattr(db_obj, attr, update_data[attr])

        db.commit()

    def delete_drama(self, db: Session, short_id: int) -> Optional[Drama]:
        obj = db.query(Drama).filter(Drama.short_id == id)
        if obj.count() == 0:
            print(f"Drama id={short_id} not found in the database")
            return None

        db.delete(obj)
        db.commit()
        return obj

