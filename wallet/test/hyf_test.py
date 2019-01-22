import requests
import json


class Hyf(object):
    def __init__(self):
        self.headers = {
            'content-type': "application/json",
            'Authorization': 'PyCharm Test'
        }
        self.payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "",
            "params": {
            
            }
        }
        self.url = "http://127.0.0.1:7000/api"
        
    def test_get_newest_message(self):
        self.payload["method"] = "get_newest_message"
        self.payload["params"] = {
            "page": "1",
            "limit": "10"
        }
        
        response = requests.post(
            self.url, data=json.dumps(self.payload), headers=self.headers).json()
        print(response)

    def test_get_newest_protocol(self):
        self.payload["method"] = "get_newest_protocol"
        self.payload["params"] = {
            "data": 1
        }
    
        response = requests.post(
            self.url, data=json.dumps(self.payload), headers=self.headers).json()
        print(response)

    def test_add_newest_feedback(self):
        self.payload["method"] = "add_newest_feedback"
        self.payload["params"] = {
            "feedback_name": "feedback_name",
            "feedback_content": "feedback_content"
        }
    
        response = requests.post(
            self.url, data=json.dumps(self.payload), headers=self.headers).json()
        print(response)

    def test_get_newest_help_information(self):
        self.payload["method"] = "get_newest_help_information"
        self.payload["params"] = {
            "page": "1",
            "limit": "10"
        }
    
        response = requests.post(
            self.url, data=json.dumps(self.payload), headers=self.headers).json()
        print(response)


if __name__ == "__main__":
    hyf = Hyf()
    
    # 获取新消息
    hyf.test_get_newest_message()
    # 新增反馈
    hyf.test_add_newest_feedback()
    # 获取协议
    hyf.test_get_newest_protocol()
    # 获取帮助信息
    hyf.test_get_newest_help_information()
