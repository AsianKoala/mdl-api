from app import schemas
from app.database import SessionLocal
from app.models.drama import Drama, Genre, Tag
from app.scrapers.parse import DramaParser

def add_drama(db: SessionLocal, drama: Drama):
    db.add(drama)
    db.commit()
    db.refresh(drama)

def init_test_data():
    db = SessionLocal()
    parser = DramaParser()
    parser.scrape("35729-emergency-lands-of-love")
    drama, genres, tags = parser.parse_models()

    db.add_all([drama, *genres, *tags])
    db.commit()

def test_db_data():
    db = SessionLocal()
    d = db.query(Tag).first()
    s = schemas.Tag.from_orm(d)
    print(s.json())
    # print(s.json())

def main():
    # init_test_data()
    test_db_data()

if __name__ == "__main__":
    main()
