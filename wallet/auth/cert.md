# APP-创建
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "创建APP的名称",    // app名称
    "desc": "app相关的描述信息", // app的描述信息
    "create_cli_keys": false,   // [true/false]，如果为true，服务端会生成用于client的公钥和私钥， 
                                // 如果为false，需要上传公钥，私钥可选
    "create_srv_keys": false,   // [true/false]，如果为true，服务端会生成用于server的公钥和私钥，
                                // 如果为false，需要上传私钥，公钥可选
    "cli_keys_length": 4096,    // 生成用于client的钥匙长度
    "srv_keys_length": 4096,    // 生成用于server的钥匙长度
    "r_cli_publickey": true,    // 在返回结果中包含用于client中的公钥，默认不返回，只返回用于client的私钥
    "r_srv_privatekey": true,   // 在返回结果中包含用于server中的私钥，默认不返回，只返回用于server的公钥
    "cli_keys": {               // 用于client端的钥匙
         "cli_publickey": "xxx",     // 公钥
         "cli_privatekey": "xxx"     // 私钥
    },
    "srv_keys": {               // 用于server端的钥匙
         "srv_publickey": "xxx",     // 公钥
         "srv_privatekey": "xxx"     // 私钥
    },
    "ip": ["192.168.100.0/24", "192.168.100.1", "218.85.0.0/255.255.0.0"],     // 用于APP接入端，请求IP验证
    "ns": ["www.zzy.com", "*.zzy.com", "*zzy.com"],    // 用于APP接入端，请求域名验证
    "srv": ["srv1", "srv2", "srv3"],  // 用于APP开放服务的验证
    "status": 0,                      // 表示APP所处状态，功能暂定
    "time": "提交时间， 格式：Unix时间戳"   // 每次提交都必须生成新的时间
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_create",             // 创建APP接口名称
    "params": {
        "appid": "syncapp",            // 后台APP名称
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "创建成功的appid", // 创建成功的APP
    "cli_publickey": "xxx",    // 用于client的公钥，默认不返回
    "cli_privatekey": "xxx",   // 用于client的私钥，默认返回
    "srv_publickey": "xxx",    // 用于server的公钥，默认返回
    "srv_privatekey": "xxx"    // 用于server的私钥，默认不返回
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-删除
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "APP的名称",     // 要删除的APP名称
    "time": "提交时间， 格式：Unix时间戳"      
}
```
把以上请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_remove",   //删除APP接口
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "成功删除的appid"    // 返回成功删除的APP名称
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```
# APP-编辑
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "APP的名称",    // 需要修改的APP名称
    // 以下字段，可以按需要进行添加
    "desc": "XXX",           // APP描述       
    "ip": ["ip1", "ip2"],    // 全部更新，不接受增量更新
    "ns": ["ns1", "ns2"],    // 全部更新，不接受增量更新
    "srv": ["srv1", "srv2"],  // 全部更新，不接受增量更新
    "cli_publickey": "xxxx",  // 用户client端的公钥
    "cli_privatekey": "xxxx", // 用户client端的私钥
    "srv_publickey": "xxxx", // 用户server端的公钥
    "srv_privatekey": "xxxx", // 用户server端的私钥
    "status": 1,              // 状态
    "time": "提交时间， 格式：Unix时间戳" 
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_edit",      // 编辑接口名称
    "params": {
        "appid": "syncapp",   // 后台APP名称
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "成功编辑的appid"
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-获取信息
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "APP的名称",
    "field": ["ip", "ns", "srv"],    // 字段列表，值参考编辑接口（不包含time字段）
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_info",       // 信息获取接口
    "params": {
        "appid": "syncapp",    // 后台APP名称
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "成功编辑的appid",
    "ip": [],
    "ns": [],
    "srv": []
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-重置证书信息
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "app名称",
    "reset_cli_keys": true,   // true/false
    "reset_srv_keys": true,   // true/false
    "cli_keys_length": 4096,  // 钥匙长度
    "srv_keys_length": 4096,  // 钥匙长度
    "r_cli_publickey": true,  // 是否返回cli的公钥  
    "r_srv_privatekey": true  // 是否返回srv的私钥
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_reset",       // 信息获取接口
    "params": {
        "appid": "syncapp",    // 后台APP名称
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "appid的名称",
    "cli_privatekey": "xxx",
    "cli_publickey": "xxx",   // 如果r_cli_publickey为true,刚返回此项
    "srv_privatekey": "xxx",  // 如果r_srv_privatekey为true,刚返回此项
    "srv_publickey": "xxx",
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-状态统计
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appids": ["appid列表", "appid2", "appid3"],  // APP名称列表
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_status",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "data": [
        {
            "appid": "appid1",
            "request_num": 100,
            "success": 80,
            "fail": 20,
            "other": "xxx"
        },
        {
            "appid": "appid2",
            "request_num": 100,
            "success": 80,
            "fail": 20,
            "other": "xxx"
        }
    ]
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

# APP-清理Redis验证缓存
---
URL:{baseurl}/api   **[POST]**
## 请求[上行]
```json
{
    "appid": "appid",  // APP名称
    "time": "提交时间， 格式：Unix时间戳"
}
```
把请求内容转化成字符串，再对字符串进行签名和加密后：
```json
{
    "method": "bk_cleanup",
    "params": {
        "appid": "syncapp",
        "sign": "对请求内容签名后的数据",
        "data": "对请求内容进行加密后的数据"
    },
    "jsonrpc": "2.0",
    "id": 0
}
```
## 回复[下行]
### 成功(密文)
```json
{
    "result": {
        "code": "success",
        "sign": "对回复内容的签名数据",
        "data": "对回复内容的加密数据"
    },
    "id": 0,
    "jsonrpc": "2.0"
}
```
先对data中数据进行解密，再对解密结果进行验证，data字段中的数据如下：
```json
{
    "appid": "appid"  // APP名称
}
```
### 失败(明文)
```json
{
      "result": {
          "code": "fail", 
          "error": "错误说明"
      }, 
      "id": 0, 
      "jsonrpc": "2.0"
}
```

