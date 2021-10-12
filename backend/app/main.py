from typing import List, Optional
from functools import lru_cache
# print all object details
from pprint import pprint

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.config import Settings
from sql_app.database import SessionLocal, user_engine

from variables.init_vars import DB_URL

models.Base.metadata.create_all(bind=user_engine)

app = FastAPI()


# @lru_cache()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def write_log(message: str):
    with open("log.txt", mode = w) as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query{q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, 
    background_tasks: BackgroundTasks,
    q: str = Depends(get_query)
    ):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return { "message" : "Message sent." }


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


if __name__ == '__main__':
    #uvicorn.run(app, host="127.0.0.0", port=8000)
    pass
