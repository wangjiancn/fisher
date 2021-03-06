# coding = utf-8
from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):  # 继承Model
    id = Column(Integer, primary_key=True, autoincrement=True)  # autoincrement自增长
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='佚名')
    binding = Column(String(50))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
