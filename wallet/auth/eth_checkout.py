# coding:utf-8
import datetime
import functools
import hashlib
import IPy
import re
import json
from wallet.util.dbmanager import db_manager
from wallet.util.redisdb import redis_store
from wallet.util.mysqldb import Apps
from wallet.auth.eth_certs import EthCert
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


def check_conn(request):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if "appid" not in kw or "data" not in kw or 'sign' not in kw:
                return {"code": "fail", "error": "data format error!"}
            # 哈希data数据，限制多次请求的问题
            sha1 = hashlib.sha1()
            sha1.update(kw['sign'].encode())
            this_hash = sha1.hexdigest()
            faster_rc = "rfaster_check_{0}".format(kw['appid'])
            try:
                if redis_store.exists(faster_rc) == 0:
                    redis_store.hset(faster_rc, this_hash, 1)
                    redis_store.expire(faster_rc, 60 * 60 * 12)
                else:
                    if redis_store.hexists(faster_rc, this_hash) is True:
                        return {"code": "fail", "error": "request faster"}
                redis_store.hset(faster_rc, this_hash, 1)
            except Exception as e:
                return {"code": "fail", "error": "redis server error!"}
            # 查询appid
            keystatus, res_kes = get_keys(kw['appid'])
            if keystatus is not True:
                return res_kes
            # srv
            if request.is_json is False:
                # 要求Content-Type为：application/json
                return {"code": "fail", "error": "content type error!"}
            if "method" not in request.json or not request.json['method']:
                return {"code": "fail", "error": "method error!"}
            if request.json['method'] not in res_kes["srv"]:
                return {"code": "fail", "error": "forbidden!"}
            # 检查客户端IP地址
            try:
                for ip_net in res_kes["ip"]:
                    if request.remote_addr in IPy.IP(ip_net):
                        break
                else:
                    return {"code": "fail", "error": "illegal ip request"}
            except Exception as e:
                return {"code": "fail", "error": f"match ip error: {e}"}

            # 检查客户端请求域名
            if ":" in request.host:
                if request.host[-1] == ']':
                    real_host = request.host
                else:
                    real_host = request.host[:request.host.rfind(":")]
            else:
                real_host = request.host
            ns_re = '(' + '|'.join(res_kes["ns"]) + ')$'
            ns_re = ns_re.replace(".", "\.").replace("*", ".*?").replace('[', '\[').replace(']', '\]')
            try:
                if not re.match(ns_re, real_host, re.I):
                    return {"code": "fail", "error": "illegal domain request"}
            except Exception as e:
                return {"code": "fail", "error": f"match domain error: {e}"}
            # 客户端
            ec_cli = EthCert()
            ec_cli.init_key(public_key_str=res_kes["keys"][0], private_key_str=res_kes["keys"][1])
            ec_cli.serialization()
            # 服务端
            ec_srv = EthCert()
            ec_srv.init_key(public_key_str=res_kes["keys"][2], private_key_str=res_kes["keys"][3])
            ec_srv.serialization()
            if kw.get("no_decrypt", None) != "no_decrypt":
                # 用自己的私钥解密
                decrypt_data = ec_srv.decrypt(kw['data'])
                if not decrypt_data:
                    return {"code": "fail", "error": ec_srv.error}
                # 用app的公钥对解密数据进行验证签名
                if "sign" not in kw:
                    return {"code": "fail", "error": "need sign data!"}
                if not ec_cli.verify(decrypt_data, kw['sign']):
                    return {"code": "fail", "error": ec_cli.error}
                try:
                    kw['decrypt'] = json.loads(decrypt_data.decode())
                except Exception as e:
                    return {"code": "fail", "error": f"need json or json error: {e}"}
            else:
                # 用app的公钥对解密数据进行验证签名
                if "sign" not in kw:
                    return {"code": "fail", "error": "need sign data!"}
                if not ec_cli.verify(kw["data"], kw['sign']):
                    return {"code": "fail", "error": ec_cli.error}
            kw['verify'] = True
            kw['ec_cli'] = ec_cli
            kw['ec_srv'] = ec_srv
            return func(*args, **kw)
        return wrapper
    return decorator


def delete_checkout_redis(appid):
    checkout_keys = "checkout_{0}_keys".format(appid)
    checkout_ns = "checkout_{0}_ns".format(appid)
    checkout_ip = "checkout_{0}_ip".format(appid)
    checkout_srv = "checkout_{0}_srv".format(appid)
    # faster_rc = "rfaster_check_{0}".format(appid)
    checkout_update = "checkout_{0}_update".format(appid)
    redis_store.delete(checkout_keys, checkout_ns, checkout_ip, checkout_srv, checkout_update)


def get_keys(appid):
    checkout_keys = "checkout_{0}_keys".format(appid)
    checkout_ns = "checkout_{0}_ns".format(appid)
    checkout_ip = "checkout_{0}_ip".format(appid)
    checkout_srv = "checkout_{0}_srv".format(appid)
    checkout_update = "checkout_{0}_update".format(appid)
    res_kes = {
        "keys": None,
        "ns": None,
        "ip": None,
        "srv": None
    }
    if redis_store.exists(checkout_keys) == 0:
        session = db_manager.slave()
        try:
            app = session.query(Apps).filter(Apps.appid == appid).one()
            session.close()
        except MultipleResultsFound:
            return False, {"code": "fail", "error": "appid fount many"}
        except NoResultFound:
            return False, {"code": "fail", "error": "appid no found"}
        except Exception as e:
            return False, {"code": "fail", "error": f"{e}"}
        res_kes["keys"] = [
                app.cli_publickey,
                app.cli_privatekey,
                app.srv_publickey,
                app.srv_privatekey,
        ]
        redis_store.delete(checkout_keys, checkout_ns, checkout_ip, checkout_srv)
        redis_store.rpush(checkout_keys, res_kes["keys"][0], res_kes["keys"][1], res_kes["keys"][2], res_kes["keys"][3])
        res_kes["ns"] = app.ns
        res_kes["ip"] = app.ip
        res_kes["srv"] = app.srv
        if res_kes["ns"]:
            redis_store.rpush(checkout_ns, *res_kes["ns"])
        if res_kes["ip"]:
            redis_store.rpush(checkout_ip, *res_kes["ip"])
        if res_kes["srv"]:
            redis_store.rpush(checkout_srv, *res_kes["srv"])
        redis_store.set(checkout_update, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        res_kes["keys"] = redis_store.lrange(checkout_keys, 0, 3)
        res_kes["ns"] = redis_store.lrange(checkout_ns, 0, -1)
        res_kes["ip"] = redis_store.lrange(checkout_ip, 0, -1)
        res_kes["srv"] = redis_store.lrange(checkout_srv, 0, -1)
    return True, res_kes



