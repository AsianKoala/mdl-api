from app.models.drama import Tag


class CRUDTag:
    ATTR_UNION = Tag | Tag

    # def get_tags(
    #         self,
    #         db: Session,
    #         offset: int = 0,
    #         limit: int = 0,
    #         search: Optional[str] = None
    #         ) -> List[TagBase]:
    #     query = db.query(Tag)
    #     if search:
    #         query = query.filter(Tag.title.ilike(f"%{search}%"))
    #     query = query.offset(offset).limit(limit).all()
    #     return query
    #
    # def get_tag(
    #         self,
    #         db: Session,
    #         title: str
    #         )
