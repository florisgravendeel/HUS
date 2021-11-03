from typing import Any, List, Optional

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, Query, Body
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

import json
import uvicorn
import os

from mailing.send_mail import simple_send, send_in_background, send_with_template, EmailSchema
from starlette.responses import JSONResponse
# from functools import lru_cache

from variables.config import Settings, settings

from tags import tags_metadata

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata)


# @lru_cache()
# def get_settings():
#     return config.Settings()



@app.get("/info")
async def info():
    return {settings.db_url,settings.mail_username}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def main():
    ban = {"message":"Welcome"}
    return ban


def mail_output(output):
    if output == True:
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    return JSONResponse(status_code=500, content=output)


@app.post("/email", tags=["send_email"])
async def send_template_mail(subject, email: EmailSchema):
    return mail_output(await send_with_template(email, subject))

@app.post("/emailtemplate", tags=["send_email"], deprecated=True)
async def send_template_mail(subject, email: EmailSchema):
    return mail_output(await send_with_template(email, subject))

@app.post("/emailbackground", tags=["send_email"], deprecated=True)
async def send_background_mail(background_tasks: BackgroundTasks, email: EmailSchema, subject, content):
    return mail_output(await send_in_background(background_tasks, email, subject, content))

@app.post("/simplemail", tags=["send_email"], deprecated=True)
async def send_mail(email: EmailSchema, subject, content):
    return mail_output(await simple_send(email, subject, content))



@app.post("/create_company/", tags=["create_data"])
def create_company(company: schemas.CompanyBase, db: Session = Depends(get_db)):
    return crud.create_company(db=db, company=company)

@app.post("/create_building/", tags=["create_data"])
def create_building(building: schemas.BuildingBase, company_id: int, db: Session = Depends(get_db)):
    return crud.create_building(db=db, building=building, company_id=company_id)

@app.post("/create_floor/", tags=["create_data"])
def create_floor(floor: schemas.FloorBase, building_id: int, db: Session = Depends(get_db)):
    return crud.create_floor(db=db, floor=floor, building_id=building_id)

@app.post("/create_room/", tags=["create_data"])
def create_room(room: schemas.RoomBase, floor_id: int, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room, floor_id=floor_id)

@app.post("/create_sensor/", tags=["create_data"])
def create_sensor(name: str, room_id: int, recource: schemas.ResourceType, db: Session = Depends(get_db)):
    return crud.create_sensor(db=db, name=name, room_id=room_id, resource_type=recource)



@app.get("/users/") #, response_model=List[schemas.User]
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




@app.post("/clear_database/", tags=["rar_db"])
def clear_database(
        confirm_1: schemas.Confirm, confirm_2: schemas.Confirm,
        db: Session = Depends(get_db),
        confirm_3: str = Query(
            "No, please stop here!", 
            regex="^Yes, I want to continue$", 
            description="Type 'Yes, I want to continue' to confirm."
            ),
        json_name: str = Query(
            ..., 
            description="The database data will be saved in a JSON file, \
                please name it."
            )
        ):
    
    # Check if everything was confirmed
    if not confirm_1 == confirm_2 == 'yes'\
    or not confirm_3 == 'Yes, I want to continue':           
        return JSONResponse(
            status_code=400, 
            content={"message":"Not confirmed"}
            )
    
    json_path = 'dummy_data/db_saves/' + json_name + '.json'

    # check if the file name was already used
    if os.path.isfile(json_path):
        return JSONResponse(
            status_code=400, 
            content={"message":"File name already in use"}
            )

    # save the data to a file 
    data = crud.get_all_dummy(db)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # clear the database 
    if not crud.clear_db(db):
        return {"message":"deleting rows failed"}

    return {"message":"data has been erased and saved","data":data}


@app.post("/populate_w_dummy/", tags=["rar_db"])
def populate_w_dummy(
    json_file_input: str = 'small_dummy',
    db: Session = Depends(get_db)
    ):
    
    json_path = "dummy_data/" + json_file_input + ".json"

    # check if the file exists
    if not os.path.isfile(json_path):
        return JSONResponse(
            status_code=400, 
            content={"message":"File does not exist"}
            )

    # load the json file
    json_file = open(json_path)
    dummy_data = json.load(json_file)
    json_file.close()
    
    return crud.populate_w_dummy(db, dummy_data)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)