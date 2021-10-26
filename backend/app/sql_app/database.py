from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from variables.init_vars import DUMMY_DB_URL, DB_URL # when trying to use multiple databases, that's where the DUMMY_DB_URL becomes used.

SQLALCHEMY_USER_DATABASE_URL = DB_URL

if SQLALCHEMY_USER_DATABASE_URL.startswith('sqlite'):
    user_engine = create_engine(
        SQLALCHEMY_USER_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    user_engine = create_engine(
        SQLALCHEMY_USER_DATABASE_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_engine)

Base = declarative_base()
