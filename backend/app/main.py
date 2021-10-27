from typing import Any, List, Optional
from functools import lru_cache
# print all object details
from pprint import pprint

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, Query, Body
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, user_engine

from mailing.send_mail import simple_send, send_in_background, send_with_template, EmailSchema
from starlette.responses import JSONResponse

from tags import tags_metadata

models.Base.metadata.create_all(bind=user_engine)

app = FastAPI(openapi_tags=tags_metadata)


# @lru_cache()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_output(output):
    if output == True:
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    return JSONResponse(status_code=500, content=output)



@app.post("/email", tags=["send_email"])
async def send_template_mail(subject ,email: EmailSchema):
    return create_output(await send_with_template(email, subject))


@app.post("/emailtemplate", tags=["send_email"], deprecated=True)
async def send_template_mail(subject ,email: EmailSchema):
    return create_output(await send_with_template(email, subject))
    

@app.post("/emailbackground", tags=["send_email"], deprecated=True)
async def send_background_mail(background_tasks: BackgroundTasks, email: EmailSchema, subject, content):
    return create_output(await send_in_background(background_tasks, email, subject, content))


@app.post("/simplemail", tags=["send_email"], deprecated=True)
async def send_mail(email: EmailSchema, subject, content):
    return create_output(await simple_send(email, subject, content))



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
    
    # class customer:
    #     def __init__(self, href, caption):
    #         self.href = href
    #         self.caption = caption

    # boi = [customer("https://trojo.net", "The best website")]
    # gir = customer("https://w3schools.com", "The smart website")

    # array = []
    # array.append(boi)
    # array.append(gir)

    # for item in boi:
    #     print(item.href)
    #     print(item.caption)

    pass
