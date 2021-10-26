from sqlalchemy.orm import Session
from sqlalchemy.sql import func

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


def basicDBstuff(db, variable):
    db.add(variable)
    db.commit()
    db.refresh(variable)


def create_building(db: Session, building: schemas.BuildingBase, company_id: int):
    db_building = models.Building(**building.dict(), company_id=company_id)
    basicDBstuff(db, db_building)
    return db_building

def create_floor(db: Session, floor: schemas.FloorBase, building_id: int):
    db_floor = models.Floor(**floor.dict(), building_id=building_id)
    basicDBstuff(db, db_floor)
    return db_floor

def create_room(db: Session, room: schemas.RoomBase, floor_id: int):
    db_room = models.Room(**room.dict(), floor_id=floor_id)
    basicDBstuff(db, db_room)
    return db_room

def create_sensor(db: Session, name: str, room_id: int, resource_type=schemas.ResourceType):
    sensor = schemas.Sensor_Resource(name=name, status='online', resource_type=resource_type)
    db_sensor = models.Sensor(**sensor.dict(), room_id=room_id)
    basicDBstuff(db, db_sensor)
    return db_sensor