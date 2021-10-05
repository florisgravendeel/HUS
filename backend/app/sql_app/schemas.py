from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.types import Json



class UserBase(BaseModel):
    name: str
    email: str
    company_id: int

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int

    class Config:
        orm_mode = True