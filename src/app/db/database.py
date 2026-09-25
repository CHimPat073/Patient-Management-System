from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from collections.abc import Generator
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

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

