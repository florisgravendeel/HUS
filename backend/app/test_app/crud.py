from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    print(type(db))
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
        # "db":DB_URL,
        "company_ids":company_ids,
        "building_ids":building_ids,
        "floor_ids":floor_ids,
        "room_ids":room_ids,
        "sensor_ids":sensor_ids,
        }