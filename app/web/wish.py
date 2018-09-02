from flask import url_for, redirect, flash
from flask_login import current_user, login_required

from app.models.gift import Gift
from . import web
from app.models.base import db



@web.route('/my/wish')
def my_wish():
    pass


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += 0.5
            db.session.add(gift)
    else:
        flash('赠送清单或心愿清单已存在，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
