# _*_ coding: utf-8 _*_
from flask import Flask
from app.models.book import db
from flask_login import LoginManager  # 导入login

login_manager = LoginManager()

__author__ = 'bobby'
__date__ = '2019/1/11 22:31'


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    db.init_app(app)
    login_manager.init_app(app)  # 初始化login_manager
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)



