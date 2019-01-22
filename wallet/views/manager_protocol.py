# coding:utf-8
import json
from flask import request
from wallet.create_app import app
from flask import render_template, jsonify
from wallet.util.dbmanager import db_manager
from wallet.util.mysqldb import Protocol
from sqlalchemy.orm.exc import MultipleResultsFound
import datetime


@app.route('/get_protocol', methods=["POST", "GET"])
def get_protocol():
    if request.method == "GET":
        try:
            start = int(request.args.get("start", "0"))
            limit = int(request.args.get("limit", "15"))
            pageIndex = int(request.args.get("pageIndex", "15"))
            session = db_manager.slave()
            p_list = session.query(Protocol).order_by(-Protocol.edit_time)[pageIndex * limit:(pageIndex + 1) * limit]
            count = session.query(Protocol).distinct().count()
            data = [{"id": p.protocol_id, "protocol_name": p.protocol_name, "protocol_content": p.protocol_content,
                     "edit_time": p.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for p in p_list]
            return jsonify({"rows": data, "results": count})
        except Exception as e:
            return jsonify({"code": f"{e}"})


@app.route('/add_protocol', methods=["POST", "GET"])
def add_protocol():
    try:
        protocol_name = request.args.get("protocol_name", None)
        protocol_content = request.args.get("protocol_content", "")
        if protocol_name:
            session = db_manager.master()
            p = Protocol(protocol_name=protocol_name, protocol_content=protocol_content, edit_time=datetime.datetime.now())
            session.add(p)
            session.commit()
            return jsonify({"code": "success"})
        else:
            return jsonify({"code": "fail"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": f"{e}"})


@app.route('/update_protocol', methods=["POST", "GET"])
def update_protocol():
    id = request.args.get("id", None)
    protocol_name = request.args.get("protocol_name", None)
    protocol_content = request.args.get("protocol_content", "")
    if not id or not protocol_name:
        return jsonify({"code": "fail", "error": "no id or msg_name"})
    try:
        session = db_manager.master()
        p = session.query(Protocol).filter(Protocol.id == id).one()
        p.protocol_name = protocol_name
        p.protocol_content = protocol_content
        session.add(p)
        session.commit()
        session.close()
        return jsonify({"code": "success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})


@app.route("/delete_protocol", methods=["POST", "GET"])
def delete_protocol():
    p_id = request.args.get("ids[]", None)
    if not p_id:
        return jsonify({"code": "fail", "error": "no id"})
    try:
        session = db_manager.master()
        p = session.query(Protocol).filter(Protocol.protocol_id == int(p_id)).delete()
        session.commit()
        session.close()
        return jsonify({"code": "delete success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})




