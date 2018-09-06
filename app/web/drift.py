from flask import flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.forms.book import DriftForm
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftViewModel, DriftCollection
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_yourself_gift(current_gift.id):
        flash('不能向自己索要书籍哦')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    if not current_user.can_send_drift():
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(current_user.email, '有人向你索要书籍', 'email/get_gift.html', wisher=current_user, gift=current_gift)

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    view_model = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=view_model.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
        拒绝请求，只有书籍赠送者才能拒绝请求
        注意需要验证超权
    """
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        # 当收到一个请求时，书籍不会处于锁定状态, 也就是说一个礼物可以收到多个请求
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
# 超权   用户可能伪造url修改路由 直接赋值给did变量，直接操作他们drift，login_required只能判断用户是否为当前脚本
def redraw_drift(did):
    with db.auto_commit():
        # todo 弹出超权提示
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """
        确认邮寄，只有书籍赠送者才可以确认邮寄
        注意需要验证超权
    """
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += current_app.config['BEANS_EVERY_DRIFT']
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        # 不查询直接更新;这一步可以异步来操作
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)  # 表单数据复制到指定对象，确保form内字段与对象内字段一致
        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        # try:
        current_user.beans -= 1
        # except Exception as e:
        # return render_template('not_enough_beans.html', beans=current_user.beans)
        db.session.add(drift)
