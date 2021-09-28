from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.types import Json



class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

# --

class NoteBase(BaseModel):
    creator_id: int
    report_id: int
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    note_id: int
    created_on: datetime
    edited_by: int
    edited_on: datetime

    class Config:
        orm_mode = True

# --

class ReportBase(BaseModel):
    report_id: int
    report_date: datetime
    data: Json

class ReportCreate(ReportBase):
    company_id: int

class Report(ReportBase):
    notes = List[Note] = [] # [Note]

    class Config:
        orm_mode = True
