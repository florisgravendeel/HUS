from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.type_api import NULLTYPE

from pydantic import BaseModel, Field
from pydantic.types import Json

from enum import Enum


class ResourceType(str, Enum):
    kilowattuur = "kilowattuur"
    co2 = "co2"
    temperatuur = "temperatuur"


class SensorStatus(str, Enum):
    online = "online"
    offline = "offline"


# All names have to correspond with the model names.

class UserBase(BaseModel):
    name: str
    email: str
    company_id: int

class UserCreate(UserBase):
    password: str
    phone_number: Optional[str] = None
    is_admin: Optional[bool] = False

class User(BaseModel):
    user_id: int
    name: str

    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Company(CompanyBase):
    company_id: int


class BuildingBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Building(BuildingBase):
    building_id: int
    company_id: int


class FloorBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Floor(FloorBase):
    floor_id: int
    building_id: int


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Room(RoomBase):
    room_id: int
    floor_id: int


class SensorBase(BaseModel):
    name: str
    status: str = "online"

    class Config:
        orm_mode = True

class Sensor_Resource(SensorBase):
    resource_type: str


class Sensor(SensorBase):
    sensor_id: int
    room_id: int
    resource_type: str

class Sensor_Group(SensorBase):
    group_address: Optional[str] = None
