from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import Generator
from app.core.config import settings


db_url = settings.database_url

if not db_url:
	raise RuntimeError("DATABASE_URL is not set in the environment")

engine = create_engine(db_url)
Session = sessionmaker(autoflush=False, bind=engine)


def get_db() -> Generator:
	db = Session()
	try:
		yield db
	finally:
		db.close()

