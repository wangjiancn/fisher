# coding = utf-8
class BookViewModel():
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls._cut_book_data(data)]
        pass

    @classmethod
    def package_collection(cls, data,keyword):
        returned = {
            'books':[],
            'total':0,
            'keyword':keyword
        }
        if data:
            returned['total']:len(data['books'])
            returned['books']:[cls._cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def _cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'],
            'author': '、'.join(data['author']), #用join处理后本地不方便操作，保存列表可以给js处理
            'price': data['price'],
            'summary': data['summary'],
            'image': data['image'],
        }
        return book
