# coding:utf-8
import json
from flask import request
from wallet.create_app import app
from flask import render_template, jsonify
from wallet.util.dbmanager import db_manager
from wallet.util.mysqldb import Message
from sqlalchemy.orm.exc import MultipleResultsFound
import datetime


@app.route('/get_message', methods=["POST", "GET"])
def get_message():
    if request.method == "GET":
        try:
            start = int(request.args.get("start", "0"))
            limit = int(request.args.get("limit", "15"))
            pageIndex = int(request.args.get("pageIndex", "15"))
            session = db_manager.slave()
            msg_list = session.query(Message).order_by(-Message.edit_time)[pageIndex*limit:(pageIndex+1)*limit]
            count = session.query(Message).distinct().count()
            data = [{"id": m.id, "msg_name": m.msg_name, "msg_content": m.msg_content,
                     "edit_time": m.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for m in msg_list]
            return jsonify({"rows": data, "results": count})
        except Exception as e:
            return jsonify({"code": f"{e}"})


@app.route('/add_message', methods=["POST", "GET"])
def add_message():
    try:
        msg_name = request.args.get("msg_name", None)
        msg_content = request.args.get("msg_content", "")
        if msg_name:
            session = db_manager.master()
            m = Message(msg_name=msg_name, msg_content=msg_content, edit_time=datetime.datetime.now())
            session.add(m)
            session.commit()
            return jsonify({"code": "success", "hasError": True, "error": "新增成功!"})
        else:
            return jsonify({"code": "fail", "hasError": True, "error": "新增失败!"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": f"{e}"})


@app.route('/update_message', methods=["POST", "GET"])
def update_message():
    id = request.args.get("id", None)
    msg_name = request.args.get("msg_name", None)
    msg_content = request.args.get("msg_content", "")
    if not id or not msg_name:
        return jsonify({"code": "fail", "error": "no id or msg_name"})
    try:
        session = db_manager.master()
        m = session.query(Message).filter(Message.id == id).one()
        m.msg_name = msg_name
        m.msg_content = msg_content
        session.add(m)
        session.commit()
        session.close()
        return jsonify({"code": "success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})
        

@app.route("/delete_message", methods=["POST", "GET"])
def delete_message():
    msg_id = request.args.get("ids[]", None)
    if not msg_id:
        return jsonify({"code": "fail", "error": "no id"})
    try:
        session = db_manager.master()
        m = session.query(Message).filter(Message.id == int(msg_id)).delete()
        session.commit()
        session.close()
        return jsonify({"code": "delete success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})
    
        
        

