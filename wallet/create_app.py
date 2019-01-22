# coding:utf-8
from flask import Flask
from flask_cors import CORS
from wallet import config
from wallet.my_dispatcher import api
from werkzeug.contrib.fixers import ProxyFix
from wallet.util.dbmanager import db_manager
from wallet.util.redisdb import redis_store


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api.as_blueprint(url='/api'))
    # 跨域请求
    CORS(app, supports_credentials=True)
    app.config['DEBUG'] = config.DEBUG
    app.config['SQLALCHEMY_DATABASE_URI_SETTINGS'] = config.SQLALCHEMY_DATABASE_URI_SETTINGS
    app.config['REDIS_URL'] = config.REDIS_URL
    app.config['APK_ROOT_DIR'] = config.APK_ROOT_DIR
    app.config['APK_DL_URL'] = config.APK_DL_URL
    return app


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

with app.app_context():
    db_manager.init_app(app)
    redis_store.init_app(app)
    # create_tables()   # 手动创建数据库表

