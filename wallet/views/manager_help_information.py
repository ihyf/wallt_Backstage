# coding:utf-8
import json
from flask import request
from wallet.create_app import app
from flask import render_template, jsonify
from wallet.util.dbmanager import db_manager
from wallet.util.mysqldb import HelpInformation
from sqlalchemy.orm.exc import MultipleResultsFound
import datetime


@app.route('/get_help_information', methods=["POST", "GET"])
def get_help_information():
    if request.method == "GET":
        try:
            start = int(request.args.get("start", "0"))
            limit = int(request.args.get("limit", "15"))
            pageIndex = int(request.args.get("pageIndex", "15"))
            session = db_manager.slave()
            h_list = session.query(HelpInformation).order_by(-HelpInformation.edit_time)[pageIndex * limit:(pageIndex + 1) * limit]
            count = session.query(HelpInformation).distinct().count()
            data = [{"id": h.hi_id, "question": h.question, "answer": h.answer,
                     "edit_time": h.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for h in h_list]
            return jsonify({"rows": data, "results": count})
        except Exception as e:
            return jsonify({"code": f"{e}"})


@app.route('/add_help_information', methods=["POST", "GET"])
def add_help_information():
    try:
        question = request.args.get("question", None)
        answer = request.args.get("answer", "")
        if question:
            session = db_manager.master()
            h = HelpInformation(question=question, answer=answer, edit_time=datetime.datetime.now())
            session.add(h)
            session.commit()
            return jsonify({"code": "success"})
        else:
            return jsonify({"code": "fail"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": f"{e}"})


@app.route('/update_help_information', methods=["POST", "GET"])
def update_help_information():
    id = request.args.get("id", None)
    question = request.args.get("question", None)
    answer = request.args.get("answer", "")
    if not id or not question:
        return jsonify({"code": "fail", "error": "no id or question"})
    try:
        session = db_manager.master()
        h = session.query(HelpInformation).filter(HelpInformation.hi_id == id).one()
        h.question = question
        h.answer = answer
        session.add(h)
        session.commit()
        session.close()
        return jsonify({"code": "success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})


@app.route("/delete_help_information", methods=["POST", "GET"])
def delete_help_information():
    hi_id = request.args.get("ids[]", None)
    if not hi_id:
        return jsonify({"code": "fail", "error": "no id"})
    try:
        session = db_manager.master()
        h = session.query(HelpInformation).filter(HelpInformation.hi_id == int(hi_id)).delete()
        session.commit()
        session.close()
        return jsonify({"code": "delete success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})




