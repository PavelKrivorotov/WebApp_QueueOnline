from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import FASTAPI_DATABASE_URL

engine = create_engine(FASTAPI_DATABASE_URL)

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
