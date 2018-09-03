# coding = utf-8
# from collections import namedtuple
from .book import BookViewModel


# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyGifts():
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.gifts = self.__parse(gifts_of_mine, wish_count_list)

    def __parse(self, gifts, wish):
        temp_gifts = []
        for gift in gifts:
            my_gift = self.__matching(gift, wish)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift, wish):
        count = 0
        for wish_count in wish:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        my_gift = {
            'id': gift.id,
            'book': BookViewModel(gift.book),
            'wishes_count': count
        }
        return my_gift
