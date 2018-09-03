# coding = utf-8
from app.view_models.book import BookViewModel


class MyWishes():
    def __init__(self, wishes_of_mine, gifts_count_list):
        self.wishes = []
        self.wishes = self.__parse(wishes_of_mine, gifts_count_list)

    def __parse(self, wishes_of_mine, gifts_count_list):
        temp_wishes = []
        for wish in wishes_of_mine:
            my_wishes = self.__matching(wish, gifts_count_list)
            temp_wishes.append(my_wishes)
        return temp_wishes

    def __matching(self, wish, gift_count_list):
        count = 0
        for gift_count in gift_count_list:
            if wish.isbn == gift_count['isbn']:
                count = gift_count['count']
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        my_wishes = {
            'id': wish.id,
            'book': BookViewModel(wish.book),
            'wishes_count': count
        }
        return my_wishes
