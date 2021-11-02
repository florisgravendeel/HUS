from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from variables.init_vars import DB_URL

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@161.35.153.83:5432/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
