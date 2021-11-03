from typing import Set
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from variables.config import settings


print(settings.db_url)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@161.35.153.83:5432/dummy"

if SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
    user_engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)
