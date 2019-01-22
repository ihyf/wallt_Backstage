# coding:utf-8
import json
from flask import request
from wallet.util.dbmanager import db_manager
from wallet.my_dispatcher import api_add
from wallet.util.mysqldb import AboutUs, SlideShow, Apk
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


@api_add
def apk_info(*args, **kwargs):
    result = {}
    session = db_manager.slave()
    try:
        apks = session.query(Apk).order_by(Apk.id.desc()).limit(1)
    except Exception as e:
        result["data"] = {}
        result["code"] = "server error"
        return result
    for apk in apks:
        info = {
            "version_number": apk.version_number,
            "version_name": apk.version_name,
            "filename": apk.filename,
            "description": apk.description,
            "download_url": apk.download_url,
            "apk_size": apk.apk_size,
            "upload_time": apk.upload_time
        }
        result["data"] = info
        break
    result["code"] = "success"
    return result


@api_add
def slideshow_info(*args, **kwargs):
    result = {}
    session = db_manager.slave()
    try:
        slideshows = session.query(SlideShow).order_by(SlideShow.id.desc()).limit(1)
    except Exception as e:
        result["data"] = {}
        result["code"] = "server error"
        return result
    for slideshow in slideshows:
        info = {
            "name": slideshow.slide_show_name,
            "description": slideshow.description,
            "time": slideshow.edit_time,
            "images": slideshow.images,
        }
        result["data"] = info
        break
    result["code"] = "success"
    return result





