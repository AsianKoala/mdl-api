from typing import List, Optional

from schemas.drama import GenreBase
from sqlalchemy.orm import Session

from app.models.drama import Genre, Tag


class CRUDGenre:
    ATTR_UNION = Tag | Genre

    def get_genres(
        self, db: Session, offset: int = 0, limit: int = 0, search: Optional[str] = None
    ) -> List[GenreBase]:
        query = db.query(Genre)
        if search:
            query = query.filter(Genre.title.ilike(f"%{search}%"))
        query = query.offset(offset).limit(limit).all()
        return query
