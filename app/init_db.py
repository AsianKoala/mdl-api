import schemas
from .database import SessionLocal
from .scrapers.parse import DramaParser

def add_drama(db: SessionLocal, drama: schemas.Drama):
    db.add(drama)
    db.commit()
    db.refresh(drama)


def init_test_data():
    db = SessionLocal()
    parser = DramaParser()
    parser.scrape("35729-emergency-lands-of-love")
    drama, genres, tags = parser.parse_model()

    db.add(drama)
    db.add_all(genres)
    db.add_all(tags)

    db.commit()
    db.refresh(drama)

def main():
    init_test_data()

if __name__ == "__main__":
    main()
