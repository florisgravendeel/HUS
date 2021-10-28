from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import true

from .database import Base


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hsd_pwd = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False) # cross db foreignkey?  --> manual ID checking
    is_admin = Column(Boolean, nullable=False, default=False)


class Company(Base):

    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)

    buildings = relationship("Building", back_populates="company")


class Building(Base):

    __tablename__ = 'building'

    building_id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    # ip_address = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey('company.company_id'),nullable=False)

    company = relationship("Company", back_populates="buildings")
    floors = relationship("Floor", back_populates="building")


class Floor(Base):

    __tablename__ = 'floor'

    floor_id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey('building.building_id'), nullable=False)

    building = relationship("Building", back_populates="floors")
    rooms = relationship("Room", back_populates="floor")


class Room(Base):

    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    floor_id = Column(Integer, ForeignKey('floor.floor_id'), nullable=False)

    floor = relationship("Floor", back_populates="rooms")
    sensors = relationship("Sensor", back_populates="room")


class Sensor(Base):

    __tablename__ = 'sensor'

    sensor_id = Column(Integer, primary_key=True, nullable=False, index=True)
    room_id = Column(Integer, ForeignKey('room.room_id'), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    group_address = Column(String, nullable=True)

    room = relationship("Room", back_populates="sensors")

