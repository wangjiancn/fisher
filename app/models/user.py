# coding = utf-8

from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from flask_login import UserMixin

from app import login_manager

# UserMixin get_id默认用’id‘键作为默认参数
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_api import YuShuBook


class User(UserMixin, Base):
    # __tablename__ = 'user'
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
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) == 'key':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
