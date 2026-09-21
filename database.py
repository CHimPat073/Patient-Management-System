from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
	raise RuntimeError("DATABASE_URL is not set in the environment")

engine = create_engine(db_url)
Session = sessionmaker(autoflush=False, bind=engine)

