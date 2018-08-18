# coding = utf-8
from flask import jsonify, Blueprint, request
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_api import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel, BookCollection

web = Blueprint('web', __name__)


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
            yushu_book.search_keyword(q)

        books.fill(yushu_book, q)
        return jsonify(books)  # 标准库json实现 return json.dumps(result),200,{'content-type':'application/json'}
    else:
        return jsonify(form.errors)
