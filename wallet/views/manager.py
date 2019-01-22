# coding:utf-8
import json
import os
from flask import request
from wallet.create_app import app
from flask import render_template, jsonify
from wallet.util.dbmanager import db_manager
from wallet.util.mysqldb import AboutUs, SlideShow, Apk
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return ""


@app.route('/main/test/', methods=["POST", "GET"])
def test():
    if request.method == "POST":
        a = request
        b = 1
    return render_template('test.html')


@app.route('/main/slideshow/', methods=['GET'])
def slideshow():
    return render_template('slideshow.html')


@app.route('/main/feedback/', methods=['GET'])
def feedback():
    return render_template('feedback.html')


@app.route('/main/help_information/', methods=['GET'])
def help_information():
    return render_template('help_information.html')


@app.route('/main/protocol/', methods=['GET'])
def protocol():
    return render_template('protocol.html')


@app.route('/main/aboutus/', methods=['GET'])
def aboutus():
    return render_template('aboutus.html')


@app.route('/main/message/', methods=["POST", "GET"])
def message():
    return render_template('message.html')


@app.route('/firstpage/', methods=['GET'])
def firstpage():
    return render_template('firstpage.html')


@app.route('/main/app/', methods=['POST', 'GET'])
def app_fun():
    return render_template('apk.html')


@app.route('/main/api/aboutus/', methods=['POST', 'GET'])
def api_aboutus():
    if request.method == 'POST':
        if request.is_json is False:
            # 要求Content-Type为：application/json
            return jsonify({"code": "fail", "error": "content type error!"})
        request_js = request.json
        for f in ["appid", "editer", "content"]:
            if f not in request_js:
                return jsonify({"code": "fail", "error": "data error!"})
        desc = request_js.get("desc", "")
        session = db_manager.master()
        try:
            aboutus = session.query(AboutUs).filter(AboutUs.appid == request_js['appid']).one()
            aboutus.appid = request_js['appid']
            aboutus.desc = desc
            aboutus.editer = request_js['editer']
            aboutus.content = request_js['content']
        except MultipleResultsFound:
            return jsonify({"code": "fail", "error": "appid fount many"})
        except NoResultFound:
            aboutus = AboutUs(
                appid=request_js['appid'],
                desc=desc,
                editer=request_js['editer'],
                content=request_js['content'],
            )
        except Exception as e:
            return jsonify({"code": "fail", "error": f"{e}"})
        session.add(aboutus)
        session.commit()
        session.close()
        return jsonify({"code": "success"})
    elif request.method == "GET":
        appid = request.args.get('appid', None)
        if appid is None:
            return jsonify({"code": "fail", "error": "data error!"})
        session = db_manager.slave()
        try:
            aboutus = session.query(AboutUs).filter(AboutUs.appid == appid).one()
            session.close()
        except MultipleResultsFound:
            return jsonify({"code": "fail", "error": "appid fount many"})
        except NoResultFound:
            return jsonify({"code": "fail", "error": "appid no found"})
        except Exception as e:
            return jsonify({"code": "fail", "error": f"{e}"})
        return jsonify({
            "appid": aboutus.appid,
            "desc": aboutus.desc,
            "editer": aboutus.editer,
            "edit_time": aboutus.edit_time,
            "content": aboutus.content,
        })
    else:
        return jsonify({"code": "fail", "error": "method no support!"})


@app.route('/main/api/slideshow/', methods=['POST', 'GET'])
def api_slideshow():
    if request.method == 'POST':
        if not request.is_json:
            return
        pjs = request.json
        session = db_manager.master()
        if 'isNew' in pjs:
            slideshow = SlideShow(
                slide_show_name=pjs['slide_show_name'],
                description=pjs['description'],
                images=pjs['pics']
            )
            session.add(slideshow)
            session.commit()
            session.close()
            return jsonify({"result": "ok"})
        else:
            try:
                slideshow = session.query(SlideShow).filter(SlideShow.id == pjs['id']).one()
                if "containspics" in pjs and pjs['containspics'] == "yes":
                    slideshow.images = pjs['pics']
                slideshow.description = pjs['description']
                slideshow.slide_show_name = pjs['slide_show_name']
            except MultipleResultsFound:
                return jsonify({"result": "appid fount many"})
            except NoResultFound:
                slideshow = SlideShow(
                    slide_show_name=pjs['slide_show_name'],
                    description=pjs['description'],
                    images=pjs['pics']
                )
                session.add(slideshow)
            except Exception as e:
                return jsonify({"result": f"{e}"})
            session.commit()
            session.close()
            return jsonify({"result": "ok"})
    elif request.method == 'GET':
        # http://localhost:7000/main/api/slideshow/?start=0&limit=30&pageIndex=0&_=1547524941956
        if "ids[]" in request.args:
            ids = request.args.getlist("ids[]")
            session = db_manager.master()
            session.query(SlideShow).filter(SlideShow.id.in_(ids)).delete(synchronize_session=False)
            session.commit()
            session.close()
            return "ok"
        else:
            session = db_manager.slave()
            slideshow = session.query(SlideShow).order_by(SlideShow.id.desc())  # .slice(start, start + limit)
            session.close()
            start = int(request.args.get('start', 0))
            limit = int(request.args.get('limit', 10))
            pageindex = int(request.args.get('pageIndex', 0))
            response = {"rows": [], "results": slideshow.count()}
            for s in slideshow.slice(start, start + limit):
                row = {
                    'id': s.id,
                    'slide_show_name': s.slide_show_name,
                    'description': s.description,
                    'edit_time': s.edit_time.timestamp(),
                    'images_num': len(s.images),
                    'images': s.images
                }
                response["rows"].append(row)
            return jsonify(response)


@app.route('/main/api/apk/', methods=['POST', 'GET'])
def api_apk():
    if request.method == "GET":
        if "ids[]" in request.args:
            ids = request.args.getlist("ids[]")
            session = db_manager.master()
            session.query(Apk).filter(Apk.id.in_(ids)).delete(synchronize_session=False)
            session.commit()
            session.close()
            return "ok"
        session = db_manager.slave()
        apks = session.query(Apk).order_by(Apk.id.desc())  # .slice(start, start + limit)
        start = int(request.args.get('start', 0))
        limit = int(request.args.get('limit', 10))
        pageindex = int(request.args.get('pageIndex', 0))
        response = {"rows": [], "results": apks.count()}
        for s in apks.slice(start, start + limit):
            row = {
                'id': s.id,
                'version_number': s.version_number,
                'version_name': s.version_name,
                'filename': s.filename,
                'description': s.description,
                'download_url': s.download_url,
                'apk_size': s.apk_size,
                'upload_time': s.upload_time.timestamp(),
            }
            response["rows"].append(row)
        return jsonify(response)
    elif request.method == "POST":
        if not request.is_json:
            return
        pjs = request.json
        session = db_manager.master()
        apk = Apk(
            version_number=pjs['version_number'],
            version_name=pjs['version_name'],
            filename=pjs['info']['filename'],
            description=pjs['description'],
            download_url=app.config['APK_DL_URL'] + pjs['info']['filename'],
            apk_size=pjs['info']['size'],
        )
        session.add(apk)
        session.commit()
        session.close()
        return jsonify({"result": "ok"})


@app.route('/main/api/upload-file/', methods=['GET', 'POST'])
def upload_file():
    save_abs_file = os.path.join(app.config['APK_ROOT_DIR'], request.files['apk'].filename)
    try:
        request.files['apk'].save(save_abs_file)
        return jsonify({"result": "ok"})
    except Exception as e:
        return jsonify({"result": "bad", "error": f"{e}"})

