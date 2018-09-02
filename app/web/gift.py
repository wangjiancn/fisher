# coding = utf-8
from contextlib import contextmanager
from flask import flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.gift import Gift
from . import web
from app.models.base import db


@web.route('/my/gifts')
@login_required
def my_gifts():
    return 'My Gift'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
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


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
