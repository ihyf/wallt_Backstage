# coding:utf-8
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, JSON, DATETIME, ForeignKey, PickleType, LargeBinary, FLOAT
from wallet.util.dbmanager import db_manager
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Apps(Base):
    __tablename__ = 'apps'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    appid = Column(String(200), primary_key=True, nullable=False, unique=True)
    desc = Column(String(200), nullable=False)
    ip = Column(JSON, nullable=False)
    ns = Column(JSON, nullable=False)
    cli_publickey = Column(Text, nullable=False)
    cli_privatekey = Column(Text, nullable=False)
    srv_publickey = Column(Text, nullable=False)
    srv_privatekey = Column(Text, nullable=False)
    srv = Column(JSON, nullable=False)
    status = Column(Integer, nullable=False)


class AboutUs(Base):
    __tablename__ = 'aboutus'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    appid = Column(String(200), nullable=False, unique=True)
    desc = Column(String(200), nullable=True)
    editer = Column(String(200), nullable=False)
    edit_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)
    content = Column(Text, nullable=True, default="")


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    msg_name = Column(String(30), nullable=True)
    msg_content = Column(Text, nullable=True, default="")
    status = Column(String(30))
    edit_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)


class SlideShow(Base):
    __tablename__ = "slide_show"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    slide_show_name = Column(String(200), nullable=True)
    description = Column(String(500))
    images = Column(JSON, nullable=True, default=[])
    edit_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)


class Apk(Base):
    __tablename__ = "apk"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    version_number = Column(Integer, nullable=False, default=0)
    version_name = Column(String(200), nullable=False)
    filename = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    download_url = Column(String(200), nullable=False)
    apk_size = Column(FLOAT, nullable=False, default=0)
    upload_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)


class Protocol(Base):
    __tablename__ = "protocol"
    protocol_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    protocol_name = Column(String(40), nullable=True)
    protocol_content = Column(Text, nullable=True, default="")
    protocol_status = Column(String(5))
    edit_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)


class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    feedback_name = Column(String(40), nullable=True)
    feedback_content = Column(Text, nullable=True, default="")
    feedback_status = Column(String(5))
    edit_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)


class HelpInformation(Base):
    __tablename__ = "help_information"
    hi_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    question = Column(String(100), nullable=True)
    answer = Column(Text, nullable=True, default="")
    status = Column(String(5))
    edit_time = Column(DATETIME, default=datetime.now(), onupdate=datetime.now)
    

def create_tables():
    engine = db_manager.get_engine_master()
    Base.metadata.create_all(engine)


