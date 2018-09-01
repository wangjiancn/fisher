# coding = utf-8

from sqlalchemy import Integer, Boolean, Column, ForeignKey, String, SmallInteger
from app.models.base import Base
from sqlalchemy.orm import relationship


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer,ForeignKey(user.id) )
    isbn = Column(String(15), nullable=False, unique=True)
    launched = Column(Boolean, default=False)

