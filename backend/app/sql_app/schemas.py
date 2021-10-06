from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.type_api import NULLTYPE

from pydantic import BaseModel, Field
from pydantic.types import Json

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