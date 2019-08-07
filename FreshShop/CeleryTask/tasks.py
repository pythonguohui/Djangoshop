from __future__ import absolute_import
from FreshShop.celery import app
import json,requests


@app.task
def taskExample():
    print('send Email ok!')

@app.task
def add(x=1,y=2):
    return x+y


@app.task
def DingTalk():
    url="https://oapi.dingtalk.com/robot/send?access_token=a071189fb89d91efb1231c6f9751d82487ab00c734459da8d0b12e78669d4b96"

    headers={
        "Content-Type":"application/json",
        "chartset":"utf-8"
    }

    requests_data={
        "msgtype":"text",
        "text":{
            "content":"哈哈哈"
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