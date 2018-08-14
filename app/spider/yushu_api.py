# coding = utf-8
from flask import current_app
from app.libs.get_http import HTTP

class YuShuBook:
    per_page = 15
    isbn_api = 'http://t.yushu.im/v2/book/isbn/{}'  # {}可以通过format导入变量
    keyword_api = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_isbn(cls, isbn):
        url = cls.isbn_api.format(isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_keyword(cls, keyword,page=1):
        url = cls.keyword_api.format(keyword,current_app.config['PER_PAGE'],cls.calculate_start(page))
        result = HTTP.get(url)
        return result

    @staticmethod
    def calculate_start(page):
        return (page-1)*current_app.config['PER_PAGE']

