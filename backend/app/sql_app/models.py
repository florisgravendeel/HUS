from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hsd_pwd = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False) ### cross db foreignkey?
    is_admin = Column(Boolean, nullable=False, default=False)


class Note(Base):
    __tablename__ = 'note'

    note_id = Column(Integer, primary_key=True, nullable=False, index=True)
    creator_id = Column(Integer, nullable=False) ### cross db foreignkey?
    report_id = Column(Integer, ForeignKey=("report.report_id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    edited_by = Column(Integer, nullable=True) ### cross db foreignkey?
    edited_on = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    report = relationship("Report", back_populates="notes")

class Report(Base):
    __tablename__ = 'report'

    report_id = Column(Integer, primary_key=True, nullable=False, index=True)
    company_id = Column(Integer, nullable=False) # cross db foreignkey?
    report_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data = Column(String, nullable=False) # a json object like: {av-temperature: "25C",hi-temperature: "30C",lo-temperature: "20C",me-temperatuur: "4",av-kilowattuur: ... etc ... }
#                                                                av = average          hi = highest          lo = lowest           me = measurements
    
    notes = relationship("Note", back_populates="report")
