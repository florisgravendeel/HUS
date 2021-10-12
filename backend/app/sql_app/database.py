from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from variables.init_vars import DB_URL

SQLALCHEMY_USER_DATABASE_URL = DB_URL

user_engine = create_engine(
    SQLALCHEMY_USER_DATABASE_URL#, connect_args=get_setting('sqlite_args')
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_engine)

Base = declarative_base()
