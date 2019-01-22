# coding:utf-8
from wallet.create_app import app
from flask import request
from wallet.my_dispatcher import api_add
from flask import render_template
from wallet.auth.eth_checkout import check_conn
from wallet.util.dbmanager import db_manager
from wallet.util.mysqldb import Message, Protocol, Feedback, HelpInformation
from flask import jsonify
import datetime


@api_add
@check_conn(request)
def bk_create(*args, **kwargs):
    print("enter")
    return {"code": "fail", "error": "appid exist"}


@api_add
def get_newest_message(*args, **kwargs):
    # 消息
    page = kwargs.get("page", None)
    limit = kwargs.get("limit", None)
    try:
        page = int(page) - 1
        limit = int(limit)
        session = db_manager.slave()
        msg_list = session.query(Message).order_by(-Message.edit_time)[page*limit:(page+1)*limit]
        data = [{"id": m.id, "msg_name": m.msg_name, "msg_content": m.msg_content,
                 "edit_time": m.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for m in msg_list]
        print(data)
        return {"data": data}
    except Exception as e:
        return {"code": "fail", "error": f"{e}"}


@api_add
def get_newest_protocol(*args, **kwargs):
    # 协议
    try:
        session = db_manager.slave()
        p_list = session.query(Protocol).order_by(-Protocol.edit_time).all()
        data = [{"id": p.protocol_id, "protocol_name": p.protocol_name, "protocol_content": p.protocol_content,
                 "edit_time": p.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for p in p_list]
        return {"data": data}
    except Exception as e:
        return {"code": "fail", "error": f"{e}"}


@api_add
def add_newest_feedback(*args, **kwargs):
    try:
        feedback_name = kwargs.get("feedback_name", None)
        feedback_content = kwargs.get("feedback_content", "")
        if feedback_name or feedback_content:
            session = db_manager.master()
            f = Feedback(feedback_name=feedback_name, feedback_content=feedback_content,
                         edit_time=datetime.datetime.now())
            session.add(f)
            session.commit()
            return {"code": "success", "message": "feedback success"}
        else:
            return {"code": "fail", "error": "no feedback_name or no feedback_content"}
    except Exception as e:
        return {"code": "fail", "error": f"{e}"}


@api_add
def get_newest_help_information(*args, **kwargs):
    # 帮助
    page = kwargs.get("page", None)
    limit = kwargs.get("limit", None)
    try:
        page = int(page) - 1
        limit = int(limit)
        session = db_manager.slave()
        h_list = session.query(HelpInformation).order_by(-HelpInformation.edit_time)[page*limit:(page+1)*limit]
        data = [{"id": h.hi_id, "question": h.question, "answer": h.answer,
                 "edit_time": h.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for h in h_list]
        return {"data": data}
    except Exception as e:
        return {"code": "fail", "error": f"{e}"}






