# coding = utf-8
import json
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
    return render_template('search_result.html', books=books,form = form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    return render_template('book_detail.html',book = book,wishes = [],gifts=[])
