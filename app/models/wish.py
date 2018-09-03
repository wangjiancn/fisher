# coding = utf-8
from sqlalchemy import Integer, Boolean, Column, ForeignKey, String, SmallInteger, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship

from app.spider.yushu_api import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False, unique=True)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gifts_counts(cls, isbn_wish_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == False,
                                                                             Gift.isbn.in_(isbn_wish_list),
                                                                             Gift.status == 1).group_by(
            Gift.isbn).all()  # filter()接受一个条件表达式
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]

        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_isbn(self.isbn)
        return yushu_book.first
