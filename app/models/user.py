# coding = utf-8
from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from flask_login import UserMixin

from app import login_manager

# UserMixin get_id默认用’id‘键作为默认参数
from app.models.drift import Drift
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

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # LoginManager要求函数
    # def get_id(self):
    #     return self.id
    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gift_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()

        return True if floor(success_receive_count / 2) <= floor(success_gift_count) else False

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

    def generate_token(self, expiation=600):
        seria = Serializer(current_app.config['SECRET_KEY'], expiation)
        temp = seria.dumps({'id': self.id}).decode('utf8')
        return temp

    @staticmethod
    def reset_password(token, new_password):
        series = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = series.loads(token.encode('utf8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
