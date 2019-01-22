# coding:utf-8
import json
from flask import request
from wallet.create_app import app
from flask import render_template, jsonify
from wallet.util.dbmanager import db_manager
from wallet.util.mysqldb import Feedback
from sqlalchemy.orm.exc import MultipleResultsFound
import datetime


@app.route('/get_feedback', methods=["POST", "GET"])
def get_feedback():
    if request.method == "GET":
        try:
            start = int(request.args.get("start", "0"))
            limit = int(request.args.get("limit", "15"))
            pageIndex = int(request.args.get("pageIndex", "15"))
            session = db_manager.slave()
            f_list = session.query(Feedback).order_by(-Feedback.edit_time)[pageIndex * limit:(pageIndex + 1) * limit]
            count = session.query(Feedback).distinct().count()
            data = [{"id": f.feedback_id, "feedback_name": f.feedback_name, "feedback_content": f.feedback_content,
                     "edit_time": f.edit_time.strftime("%Y-%m-%d %H:%M:%S")} for f in f_list]
            return jsonify({"rows": data, "results": count})
        except Exception as e:
            return jsonify({"code": f"{e}"})


@app.route('/add_feedback', methods=["POST", "GET"])
def add_feedback():
    try:
        feedback_name = request.args.get("feedback_name", None)
        feedback_content = request.args.get("feedback_content", "")
        if feedback_name:
            session = db_manager.master()
            f = Feedback(feedback_name=feedback_name, feedback_content=feedback_content, edit_time=datetime.datetime.now())
            session.add(f)
            session.commit()
            return jsonify({"code": "success"})
        else:
            return jsonify({"code": "fail"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": f"{e}"})


@app.route('/update_feedback', methods=["POST", "GET"])
def update_feedback():
    id = request.args.get("id", None)
    feedback_name = request.args.get("feedback_name", None)
    feedback_content = request.args.get("feedback_content", "")
    if not id or not feedback_name:
        return jsonify({"code": "fail", "error": "no id or feedback_name"})
    try:
        session = db_manager.master()
        f = session.query(Feedback).filter(Feedback.feedback_id == id).one()
        f.feedback_name = feedback_name
        f.feedback_content = feedback_content
        session.add(f)
        session.commit()
        session.close()
        return jsonify({"code": "success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})


@app.route("/delete_feedback", methods=["POST", "GET"])
def delete_feedback():
    feedback_id = request.args.get("ids[]", None)
    if not feedback_id:
        return jsonify({"code": "fail", "error": "no id"})
    try:
        session = db_manager.master()
        f = session.query(Feedback).filter(Feedback.feedback_id == int(feedback_id)).delete()
        session.commit()
        session.close()
        return jsonify({"code": "delete success"})
    except Exception as e:
        print(f"{e}")
        # return jsonify({"code": "fail", "error": f"{e}"})




