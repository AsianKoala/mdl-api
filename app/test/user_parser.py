import schemas
from database import SessionLocal
from db.crud.user import CRUDUser

from app.scrapers.user import UserParser


def main():
    parser = UserParser()
    parser.scrape("koawa")
    parser.parse_model()
    crud = CRUDUser()
    db = SessionLocal()

    # crud.create_user(db, model)

    db_obj = crud.get_users(db)[0]
    user = schemas.User.from_orm(db_obj)
    print(user)


if __name__ == "__main__":
    main()
