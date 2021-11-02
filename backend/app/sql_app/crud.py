from sqlalchemy.orm import Session
# from sqlalchemy.sql import func

from variables.init_vars import DB_URL 

import pprint
from starlette.responses import JSONResponse

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


async def get_user_by_email(db: Session, email: str):
    print(type(db))
    data = await db.query(models.User).filter(email == email).first()
    return data


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_count(db: Session):
    return len(db.query(models.User.user_id).scalar())

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    print(db)
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
    # return getattr(db_user, 'user_id')
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



def create_company(db: Session, company: schemas.CompanyBase):
    db_company = models.Company(**company.dict())
    basicDBstuff(db, db_company)
    return db_company


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
    allow = check_rooms(db, room_id)
    if allow:
        sensor = schemas.Sensor_Resource(name=name, status='online', resource_type=resource_type)
        db_sensor = models.Sensor(**sensor.dict(), room_id=room_id)
        basicDBstuff(db, db_sensor)
        return db_sensor
    return JSONResponse(status_code=404, content={"message": "Room not found"})


def get_all_dummy(db: Session):
    company = db.query(models.Company).all()
    json_company = []
    for i in company:
        add_data = {}
        add_data['company_id'] = getattr(i, 'company_id')
        add_data['name'] = getattr(i, 'name')
        json_company.append(add_data)
    
    building = db.query(models.Building).all()
    json_building = []
    for i in building:
        add_data = {}
        add_data['building_id'] = getattr(i, 'building_id')
        add_data['name'] = getattr(i, 'name')
        add_data['company_id'] = getattr(i, 'company_id')
        json_building.append(add_data)
    
    floor = db.query(models.Floor).all()
    json_floor = []
    for i in floor:
        add_data = {}
        add_data['floor_id'] = getattr(i, 'floor_id')
        add_data['name'] = getattr(i, 'name')
        add_data['building_id'] = getattr(i, 'building_id')
        json_floor.append(add_data)
    
    room = db.query(models.Room).all()
    json_room = []
    for i in room:
        add_data = {}
        add_data['room_id'] = getattr(i, 'room_id')
        add_data['name'] = getattr(i, 'name')
        add_data['floor_id'] = getattr(i, 'floor_id')
        json_room.append(add_data)
    
    sensor = db.query(models.Sensor).all()
    json_sensor = []
    for i in sensor:
        add_data = {}
        add_data['sensor_id'] = getattr(i, 'sensor_id')
        add_data['name'] = getattr(i, 'name')
        add_data['room_id'] = getattr(i, 'room_id')
        add_data['resource_type'] = getattr(i, 'resource_type')
        add_data['status'] = getattr(i, 'status')
        add_data['group_address'] = getattr(i, 'group_address')
        json_sensor.append(add_data)
    
    return {
        "company": json_company,
        "building": json_building,
        "floor": json_floor,
        "room": json_room,
        "sensor": json_sensor
        }
    

def populate_w_dummy(db: Session, dummy_data):
    # return DB_URL
    # db = next(db_)  # prevents: "AttributeError: 'generator' object has no attribute 'add'"
    # source:
    # https://stackoverflow.com/questions/65982681/how-to-access-the-database-from-unit-test-in-fast-api
    company_ids = {}
    building_ids = {}
    floor_ids = {}
    room_ids = {}
    sensor_ids = {}
    for d in dummy_data:
        for i in dummy_data[d]:
            if d == "company":
                item = models.Company(
                    name=i['name']
                    )
                db.add(item)
                db.flush()
                db.refresh(item)
                company_ids[i['company_id']] = item.company_id
            
            if d == "building":
                item = models.Building(
                    name=i['name'],
                    company_id=company_ids[i['company_id']]
                    )
                db.add(item)
                db.flush()
                db.refresh(item)
                building_ids[i['building_id']] = item.building_id
            
            if d == "floor":
                item = models.Floor(
                    name=i['name'],
                    building_id=building_ids[i['building_id']]
                    )
                db.add(item)
                db.flush()
                db.refresh(item)
                floor_ids[i['floor_id']] = item.floor_id

            if d == "room":
                item = models.Room(
                    name=i['name'],
                    floor_id=floor_ids[i['floor_id']]
                    )
                db.add(item)
                db.flush()
                db.refresh(item)
                room_ids[i['room_id']] = item.room_id

            if d == "sensor":
                item = models.Sensor(
                    name=i['name'],
                    room_id=room_ids[i['room_id']],
                    resource_type=i['resource_type'],
                    status=i['status'],
                    group_address=i['group_address']
                    )
                db.add(item)
                db.flush()
                db.refresh(item)
                sensor_ids[i['sensor_id']] = item.sensor_id

    # db_building = models.Building(**building.dict(), company_id=company_id)
    # basicDBstuff(db, db_building)
    # return db_building
    return {
        "db":DB_URL,
        "company_ids":company_ids,
        "building_ids":building_ids,
        "floor_ids":floor_ids,
        "room_ids":room_ids,
        "sensor_ids":sensor_ids,
        }