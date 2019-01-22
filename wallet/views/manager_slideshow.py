# coding:utf-8
from wallet.util.dbmanager import db_manager
from wallet.util.upload import Upload
from wallet.util.mysqldb import SlideShow
from wallet.create_app import app
from flask import render_template, jsonify
from flask import request


@app.route("/get_slide_show")
def get_slide_show():
    data = [{"slide_show_name": "hahah", "description": "123", "image1": 1},
            {"slide_show_name": "hahah", "description": "123"}]
    return jsonify({"rows": data, "results": 10})


@app.route("/add_slide_show", methods=["POST", "GET"])
def add_slide_show(*args, **kwargs):
    a = request
    z = request.args.get("slide_show_name", None)
    C = request.form_data_parser_class.parse_functions
    b = 1


@app.route("/update_slide_show")
def update_slide_show():
    pass


@app.route("/delete_slide_show")
def delete_slide_show():
    pass
