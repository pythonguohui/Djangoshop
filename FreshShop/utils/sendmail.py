import smtplib
from email.mime.text import MIMEText

subject ="老郭的学习邮件"
content= "好好学习，天天向上"
sender = "385726424@qq.com"
recver="""329688391@qq.com,1056940091@qq.com"""

password="pnpxhjohfupwbjaf"

message=MIMEText(content,"plain","utf-8")
message["Subject"]=subject
message["TO"] =recver
message["From"]=sender

smtp=smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()