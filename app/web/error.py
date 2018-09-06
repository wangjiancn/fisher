# coding = utf-8
from flask import render_template

from app.web import web


@web.app_errorhandler(404)
def not_find(e):
    return render_template('404.html'), 404
