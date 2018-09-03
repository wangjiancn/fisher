# coding = utf-8
import json

from flask_login import current_user

from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo
from . import web
from flask import jsonify, Blueprint, request, render_template, flash
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_api import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel, BookCollection


@web.route('/book/search')
def search():
    '''
    ?q=<q>&page=<page>
    '''
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_isbn(q)
        else:
            yushu_book.search_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
        # return jsonify(books)  # 标准库json实现 return json.dumps(result),200,{'content-type':'application/json'}
    else:
        flash('关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 查询书籍
    yushu_book = YuShuBook()
    yushu_book.search_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True

        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
