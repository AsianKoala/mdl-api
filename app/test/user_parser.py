import requests
from app.models.user import User
import schemas
from database import SessionLocal
from db.crud.user import CRUDUser

from app.scrapers.user import UserParser


def main():
    r = requests.get("https://mydramalist.com/dramalist/koawa")
    with open("app/.cache/watchlist.html", "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    main()
