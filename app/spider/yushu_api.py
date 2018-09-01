# coding = utf-8
from flask import current_app
from app.libs.get_http import HTTP

class YuShuBook:
    isbn_api = 'http://t.yushu.im/v2/book/isbn/{}'  # {}可以通过format导入变量
    keyword_api = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_isbn(self, isbn):
        url = self.isbn_api.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_keyword(self, keyword,page=1):
        url = self.keyword_api.format(keyword,current_app.config['PER_PAGE'],self.calculate_start(page))
        # url = self.keyword_api.format(keyword,current_app.config['PER_PAGE'],1)
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        self.total = data['total']
        self.books = data['books']

    def calculate_start(self,page):
        return (page-1)*current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >=1 else None

