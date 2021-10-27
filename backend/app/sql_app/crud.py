from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from variables.init_vars import DB_URL

from starlette.responses import JSONResponse

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_count(db: Session):
    return db.query(func.count(models.User.user_id)).scalar()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        hsd_pwd=fake_hashed_password, 
        company_id=user.company_id, 
        phone_number=user.phone_number,
        is_admin=user.is_admin
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def basicDBstuff(db: Session, variable):
    db.add(variable)
    db.commit()
    db.refresh(variable)



def check_companies(db: Session, id):
    for i in db.query(models.Company):
        if i.company_id == id:
            return True
    return False

def check_buildings(db: Session, id):
    for i in db.query(models.Building):
        if i.building_id == id:
            return True
    return False

def check_floors(db: Session, id):
    for i in db.query(models.Floor):
        if i.floor_id == id:
            return True
    return False

def check_rooms(db: Session, id):
    for i in db.query(models.Room):
        if i.room_id == id:
            return True
    return False



def create_building(db: Session, building: schemas.BuildingBase, company_id: int):
    allow = check_companies(db, company_id)
    if allow:
        db_building = models.Building(**building.dict(), company_id=company_id)
        basicDBstuff(db, db_building)
        return db_building
    return JSONResponse(status_code=404, content={"message": "Building not found"})


def create_floor(db: Session, floor: schemas.FloorBase, building_id: int):
    allow = check_buildings(db, building_id)
    if allow:
        db_floor = models.Floor(**floor.dict(), building_id=building_id)
        basicDBstuff(db, db_floor)
        return db_floor
    return JSONResponse(status_code=404, content={"message": "Building not found"})


def create_room(db: Session, room: schemas.RoomBase, floor_id: int):
    allow = check_floors(db, floor_id)
    if allow:
        db_room = models.Room(**room.dict(), floor_id=floor_id)
        basicDBstuff(db, db_room)
        return db_room
    return JSONResponse(status_code=404, content={"message": "Floor not found"})


def create_sensor(db: Session, name: str, room_id: int, resource_type=schemas.ResourceType):
    allow = check_floors(db, room_id)
    if allow:
        sensor = schemas.Sensor_Resource(name=name, status='online', resource_type=resource_type)
        db_sensor = models.Sensor(**sensor.dict(), room_id=room_id)
        basicDBstuff(db, db_sensor)
        return db_sensor
    return JSONResponse(status_code=404, content={"message": "Room not found"})