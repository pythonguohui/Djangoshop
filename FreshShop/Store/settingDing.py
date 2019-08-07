import json
import requests

url="https://oapi.dingtalk.com/robot/send?access_token=a071189fb89d91efb1231c6f9751d82487ab00c734459da8d0b12e78669d4b96"

headers={
    "Content-Type":"application/json",
    "chartset":"utf-8"
}

requests_data={
    "msgtype":"text",
    "text":{
        "content":"贾宽新就是牛，酒神不是浪得虚名"
    },
    "at":{
        "atMobiles":[],
    },
    "isAtAll":True
}

sendData = json.dumps(requests_data)
response=requests.post(url,headers=headers,data=sendData)
content=response.json()
print(content)