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
