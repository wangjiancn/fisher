# coding = utf-8
from flask import Flask
from app.models.base import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    # print(app.config['STATUS'])
    app.config.from_object('app.secure')
    # print(app.config['STATUS'])
    register_blueprint(app)
    db.init_app(app)    #初始化数据库
    db.create_all(app=app)  #创建Book数据表
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)



