from flask import url_for, redirect, flash, render_template
from flask_login import current_user, login_required

from app.models.wish import Wish
from app.view_models.wish import MyWishes
from . import web
from app.models.base import db



@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_gift_list = [wish.isbn for wish in wishes_of_mine]
    wish_count_list = Wish.get_gifts_counts(isbn_gift_list)
    view_model = MyWishes(wishes_of_mine, wish_count_list)
    return render_template('my_wish.html', wishes=view_model.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('赠送清单或心愿清单已存在，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
