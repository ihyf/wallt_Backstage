# coding:utf-8
import os
DEBUG = True

SQLALCHEMY_DATABASE_URI_SETTINGS = {
    'master': [
        'mysql+pymysql://wallet:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.241/wallet?charset=utf8',
    ],
    'slave': [
        'mysql+pymysql://wallet:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.21/wallet?charset=utf8',
        'mysql+pymysql://wallet:qCx4V-3p2KYbV86o6Su4E6)43+=3.ax+@192.168.1.22/wallet?charset=utf8',
    ]
}

REDIS_URL = "redis://:@192.168.1.20:6379/1?charset=utf8&decode_responses=true"

APK_ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'apks')

APK_DL_URL = "http://192.168.1.77:7000/static/apks/"
