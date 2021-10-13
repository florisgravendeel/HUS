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