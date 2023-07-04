from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from app.models.drama import Tag


class CRUDTag:
    def get_tags(
        self, db: Session, offset: int = 0, limit: int = 0, search: Optional[str] = None
    ) -> List[Tag]:
        query = db.query(Tag)
        if search:
            query = query.filter(Tag.title.ilike(f"%{search}%"))
        query = query.offset(offset).limit(limit).all()
        return query

    def get_tag(self, db: Session, id: int) -> Optional[Tag]:
        query = db.query(Tag).filter(Tag.id == id).first()
        return query
