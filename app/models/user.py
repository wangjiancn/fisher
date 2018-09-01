# coding = utf-8

from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base
from flask_login import UserMixin


# UserMixin get_id默认用’id‘键作为默认参数
class User(UserMixin, Base):
    # __tablename__ = 'user1'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(13), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    confirmed = Column(Boolean(50), default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    # todo 装饰器用途
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # LoginManager要求函数
    # def get_id(self):
    #     return self.id
