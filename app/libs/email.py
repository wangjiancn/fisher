# coding = utf-8
from threading import Thread

from flask_mail import Message
from app import mail
from flask import current_app, render_template


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(mailto, subject, template, **kwargs):
    msg = Message('[鱼书] ' + subject, sender=current_app.config['MAIL_SENDER'], recipients=[mailto])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
