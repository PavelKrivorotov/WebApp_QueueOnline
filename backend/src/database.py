from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import db_url as url

db_url = url()
engine = create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,

)

Base = declarative_base()


def db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
