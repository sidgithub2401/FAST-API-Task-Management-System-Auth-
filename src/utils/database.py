from dotenv import load_dotenv
from sqlalchemy import create_engine
import os 
from sqlalchemy.orm import sessionmaker , declarative_base
load_dotenv()

database_connection = os.getenv("DATABASE_URL")

engine = create_engine(url = database_connection)

local_session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = local_session()
        yield db
    finally:
        db.close()

