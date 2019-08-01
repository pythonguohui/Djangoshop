import requests

url ="http://106.ihuyi.com/webservice/sms.php?method=Submit"

account = ""
password =""
mobile=""
content="您的验证码是：201981。请不要把验证码泄露给其他人。"

headers={
    "Content-type":"application/x-www-form-urlencoded",
    "Accept":"text/plain"
}

data={
    "account":account,
    "password":password,
    "mobile":mobile,
    "content":content,
}
response=requests.post(url,headers=headers,data=data)

print(response.content.decode())