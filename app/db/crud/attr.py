from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDAttr(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_models(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> List[ModelType]:
        query = db.query(ModelType)
        if search:
            query = query.filter()
