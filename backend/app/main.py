from typing import List 
from functools import lru_cache
# print all object details
from pprint import pprint

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.config import Settings
from sql_app.database import SessionLocal, user_engine

import constants
from os import environ as env
from dotenv import load_dotenv, find_dotenv


models.Base.metadata.create_all(bind=user_engine)

app = FastAPI()

print('find_dotenv: ')
print(find_dotenv)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


print('before')

# @lru_cache()
@app.get("/settings_test/")
async def settings_test():
    return env.get(constants.UDB)

print('after')



@app.get("/settings_test/s")
def settering():
    return Settings.UDB

@app.get("/oof/")
def oof():
    return pprint(vars(Settings))



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user_count/")
def count_user(db: Session = Depends(get_db)):
    return crud.get_user_count(db)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)