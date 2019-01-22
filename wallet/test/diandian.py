import requests
import json
import time
import re
from wallet.auth.eth_certs import EthCert

"""接口测试用"""


class DianDian(object):

    def __init__(self):
        self.ec_cli = EthCert("syncapp_cli")
        self.ec_cli.load_key_from_file()
        self.ec_cli.serialization()
        self.ec_srv = EthCert("syncapp_srv")
        self.ec_srv.load_key_from_file()
        self.ec_srv.serialization()

    def request(self, data):
        headers = {
            'content-type': "application/json",
            'Authorization': 'PyCharm Test'
        }
        response = requests.post("http://127.0.0.1:7000/api", data=json.dumps(data), headers=headers)
        return response.text

    def request_json(self, method, sign, encrypt):
        post_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": {
                "appid": "diandian",
                "sign": sign,
                "data": encrypt
            }
        }
        return post_data

    def check_rt(self, res):
        res_js = json.loads(res)
        print(res_js)
        if "error" in res_js:
            return res_js
        res_data = res_js['result']
        if res_data['code'] == "success":
            decrypt_data = self.ec_cli.decrypt_str(res_data['data'])
            if self.ec_srv.verify(decrypt_data, res_data['sign']):
                return decrypt_data
            else:
                return self.ec_srv.error
        else:
            return res_js

    def action(self, data, api):
        data_str = json.dumps(data, ensure_ascii=False)
        sign = self.ec_cli.sign_str(data_str)
        encrypt = self.ec_srv.encrypt_str(data_str)
        res = self.request(self.request_json(api, sign, encrypt))
        result = self.check_rt(res)
        return result

    def ck_domain(self, doamin):
        ns = []
        ns_re = '(' + '|'.join(ns) + ')$'
        ns_re = ns_re.replace(".", "\.")
        if not re.match(ns_re, doamin, re.I):
            print("No Match")
        else:
            print("Match")

    def bk_create(self, appid="None"):
        data = {
            "appid": appid,
            "desc": "测试数据_可以随意删除",
            "create_cli_keys": True,
            "create_srv_keys": True,
            "cli_keys_length": 1024,
            "srv_keys_length": 1024,
            "r_cli_publickey": False,
            "r_srv_privatekey": False,
            "cli_keys": {
                 "cli_publickey": "",
                 "cli_privatekey": ""
            },
            "srv_keys": {
                 "srv_publickey": "",
                 "srv_privatekey": ""
            },
            "ip": ["192.168.1.0/255.255.255.0", "192.168.1.2", "127.0.0.1", '192.168.1.77'],
            "ns": ["localhost", "127.0.0.1", "192.168.1.77"],
            "srv": [],
            "status": 0,
            "time": time.time()
        }
        result = self.action(data, 'bk_create')
        print("bk_create <=>", result)

    def bk_remove(self):
        data = {
            "appid": "app_test_9",
            "time": int(time.time())
        }
        result = self.action(data, 'bk_remove')
        print("bk_remove <=>", result)

    def bk_edit(self):
        data = {
            "appid": "diandian",
            "srv": [
                "bk_create",
                "bk_remove",
                "bk_edit",
                "bk_info",
                "bk_status",
                "bk_cleanup",
                "bk_reset",
            ],
            # "ns": ["全部更新，不接受增量更新", "ns2"],
            # "ip": ["全部更新，不接受增量更新", "ip2"],
            # "srv": ["全部更新，不接受增量更新", "srv2"],
            # "cli_publickey": self.ec_cli.get_publickey(),
            # "cli_privatekey": self.ec_cli.get_privatekey(),
            # "srv_publickey": self.ec_srv.get_publickey(),
            # "srv_privatekey": self.ec_srv.get_privatekey(),
            # "status": 100,
            # "lelsie": True,
            "time": time.time()
        }
        result = self.action(data, 'bk_edit')
        print("bk_edit <=>", result)

    def bk_info(self):
        data = {
            "appid": "app_test_8",
            "field": ["ip", "ns", "srv", "cli_publickey", "cli_privatekey", "srv_publickey", "srv_privatekey"],
            "time": time.time()
        }
        result = self.action(data, 'bk_info')
        print("bk_info <=>", result)

    def bk_status(self):
        data = {
            "appids": ["app_test_8", "app_test_7"],
            "time": time.time()
        }
        result = self.action(data, 'bk_status')
        print("bk_status <=>", result)

    def bk_cleanup(self):
        data = {
            "appid": "canigreen",
            "time": int(time.time())
        }
        result = self.action(data, 'bk_cleanup')
        print("bk_cleanup <=>", result)

    def bk_reset(self):
        data = {
            "appid": "test_app_10",
            "reset_cli_keys": True,
            "reset_srv_keys": True,
            "cli_keys_length": 1024,
            "srv_keys_length": 1024,
            "r_cli_publickey": False,
            "r_srv_privatekey": False,
            "time": time.time(),
        }
        result = self.action(data, 'bk_reset')
        print("bk_reset <=>", result)

    def json_test(self):
        js_strings = {
            'method': 'deploy_contract',
            'params': {
                'appid': 'syncapp',
                'sign': 'JjZyMJCnSPj9G1K5FAy50DeWeNeSNs6j/Ebz4MalSgUaDXoH7SL8LPHeFJEIhv+WaLnCtkvpsKvEFLrhZnHSuJ8S9nhk9ki12Bu6AdQN4kgqkE/3eLIACtiYu3DhMPho4ts/YqkbPOz0WT7EqF+I1CwSvOU6/yRPsTWfDW8YHkl/pz2Kczl2o+weVfjllvniXW8FhPsJSkqA82dsgG4WMbgwAYBNWFt/+31Ic/nudTTaHbqA0kwGsJ7kIQIq1BCYcmMCPeA/JNDscuVdoJaQbjSYRP6jHGqcZ/RMOBToFfIMqOdgayqPNcNcn3DJ4uu3jNVFH2sl2feVrcn7uJ0rH5JKS/cohgwdPHT3k4YQTvmLFWBoOFTLoFo3X9ZyaVyvKKfd7EMV+LYYaePoTf89DY7YaBCyasDItY8l5gOa5M4f9nxAHs/eAAR0s/TPO1cdGa5LxiRcOjv4oUBjsLgt3U1CmI37IHowBrsYP4Eu1CSIljtHxETYui429FyFvmQWB+sCrQZLKwcX9Lk6C4MFQL62Z1UOr+Qn94/vXwXCuJ2NmxMu+SuE+opaYKR3qPd3Ic5d0bY6C72rmpDDkUoWonqr7BdoVVR66oUSm2cM0Y0pM/c91x2OL+AIY+Ucyj4CnsOH/nEfA4ahFdBPkGKdHLrs4brJ0VdiUo6rLXu8+K8=',
                'data': {
                    'contract_name': 'cq_1_16',
                    'master_contract_name': 'cq_1',
                    'master_contract_address': '0xD092Da0F91294CaD6e032AE930C7c376180f3FAD',
                    'time': 1548037671
                }
            },
            'jsonrpc': '2.0',
            'id': '0'
        }
        result = json.dumps(js_strings['params']['data'], separators=(',', ':'))
        print(result)
        js_strings['mysign'] = self.ec_cli.sign_str(result)
        js_strings['strings'] = result
        return js_strings
        # print(result)
        # print(result)
        # js_strings['params']['data'] = result
        # print(result)


if __name__ == "__main__":
    dd = DianDian()
    # dd.bk_remove()
    # for i in range(5):
    #     name = f"appid_bk_inc4_{i}"
    #     dd.bk_create(appid=name)
    # dd.bk_reset()
    # dd.bk_edit()
    # dd.bk_info()
    # dd.bk_status()
    # dd.bk_cleanup()
    dd.json_test()







