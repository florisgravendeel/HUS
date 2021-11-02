from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

# when trying to use multiple databases, that's where the DUMMY_DB_URL becomes used.
from variables.init_vars import DB_URL 

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@161.35.153.83:5432/dummy"

# if SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
#     user_engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#     )
# else:
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base(bind=engine)
