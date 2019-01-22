# coding:utf-8
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBManager(object):
    def __init__(self):
        self.engine_map = {}
        self.session_map = {}

    def init_app(self, app):
        self.create_sessions(app)

    def create_sessions(self, app):
        db_settings = app.config['SQLALCHEMY_DATABASE_URI_SETTINGS']
        for role, urls in db_settings.items():
            self.engine_map[role] = []
            self.session_map[role] = []
            for url in urls:
                engin, single_session = self.create_single_session(url)
                self.engine_map[role].append(engin)
                self.session_map[role].append(single_session)

    @classmethod
    def create_single_session(cls, url, scopefunc=None):
        engine = create_engine(url, pool_recycle=7200, pool_size=50)
        return engine, scoped_session(sessionmaker(expire_on_commit=False, bind=engine), scopefunc=scopefunc)

    def get_session(self, name):
        try:
            if not name:
                # 当没有提供名字时，我们默认为读请求，
                name = 'slave'
            # 现在的逻辑是在当前所有的配置中随机选取一个数据库，
            return random.choice(self.session_map[name])
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(name))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')

    def get_engine_master(self):
        return self.engine_map['master'][0]

    def master(self):
        return random.choice(self.session_map['master'])

    def slave(self):
        return random.choice(self.session_map['slave'])

    def session_ctx(self, bind=None):
        db_session = self.get_session(bind)
        session = db_session()
        session._model_changes = {}    # ???
        return session


class DBProxy(object):
    db_session_manager = None
    write_db = None
    read_db = None

    def __init__(self, db_session_manager=None):
        self.app = None
        self.db_session_manager = db_session_manager

    def init_app(self, app):
        self.app = app

    def init_db_session(self, action='r'):
        # action in ['r', 'w', 'rw']
        try:
            self.write_db = self.db_session_manager.session_ctx(bind='master')
            self.read_db = self.db_session_manager.session_ctx()
            # 根据user_id 处理连接
            # e.g. self.write_db.execute('use db_' + user_id)
        except Exception as e:
            self.app.logger.exception('info')
        return


db_manager = DBManager()




