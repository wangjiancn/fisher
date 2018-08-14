# coding = utf-8
from flask import jsonify, Blueprint, request
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_api import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel

web = Blueprint('web', __name__)


@web.route('/book/search')
def search():
    '''
    ?q=<q>&page=<page>
    '''
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = YuShuBook.search_isbn(q)
            result = BookViewModel.package_single(result,q)
        else:
            result = YuShuBook.search_keyword(q, page)
            result = BookViewModel.package_collection(result,q)
        return jsonify(result)  # 标准库json实现 return json.dumps(result),200,{'content-type':'application/json'}
    else:
        return jsonify(form.errors)
