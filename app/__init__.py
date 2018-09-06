# coding = utf-8
from flask_login import LoginManager
from flask import Flask
from app.models.base import db
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    # print(app.config['STATUS'])
    app.config.from_object('app.secure')
    # print(app.config['STATUS'])
    register_blueprint(app)
    db.init_app(app)  # 初始化数据库
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    db.create_all(app=app)  # 创建Book数据表
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
