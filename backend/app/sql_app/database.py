from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_USER_DATABASE_URL = "postgresql://postgres:postgres@161.35.153.83:5432/user"

user_engine = create_engine(
    SQLALCHEMY_USER_DATABASE_URL # connect_agrs only needed for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_engine)

Base = declarative_base()
