from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.type_api import NULLTYPE

from pydantic import BaseModel, Field
from pydantic.types import Json

from enum import Enum


class Confirm(str, Enum):
    no = "no"
    yes = "yes"


class ResourceType(str, Enum):
    co2 = "co2"
    kilowattuur = "kilowattuur"
    temperatuur = "temperatuur"
    luchtvochtigheid = "luchtvochtigheid"


class SensorStatus(str, Enum):
    online = "online"
    offline = "offline"



class test_data(BaseModel):
    input: str


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


class BuildingBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Building(BuildingBase):
    company_id: int


class FloorBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Floor(FloorBase):
    building_id: int


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Room(RoomBase):
    floor_id: int


class SensorBase(BaseModel):
    name: str
    status: str = "online"

    class Config:
        orm_mode = True

class Sensor_Resource(SensorBase):
    resource_type: str


class Sensor(SensorBase):
    room_id: int
    resource_type: str
    group_address: Optional[str] = None
