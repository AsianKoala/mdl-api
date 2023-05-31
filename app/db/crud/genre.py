from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.drama import Genre


class CRUDGenre:
    def get_genres(
        self, db: Session, offset: int = 0, limit: int = 0, search: Optional[str] = None
    ) -> List[Genre]:
        query = db.query(Genre)
        if search:
            query = query.filter(Genre.title.ilike(f"%{search}%"))
        query = query.offset(offset).limit(limit).all()
        return query

    def get_genre(self, db: Session, id: int) -> Optional[Genre]:
        query = db.query(Genre).filter(Genre.id == id).first()
        return query
