# coding = utf-8
from flask import current_app
from sqlalchemy import Integer, Boolean, Column, ForeignKey, String, SmallInteger, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.wish import Wish
from app.spider.yushu_api import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_wish_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                                                             Wish.isbn.in_(isbn_wish_list),
                                                                             Wish.status == 1).group_by(
            Wish.isbn).all()  # filter()接受一个条件表达式
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]

        return count_list

    @classmethod
    def recent(cls):
        # 链式调用
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(10).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_isbn(self.isbn)
        return yushu_book.first
