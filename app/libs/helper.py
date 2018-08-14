# coding = utf-8

def is_isbn_or_key(word):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():  # 可能是假的条件放在前面
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key

