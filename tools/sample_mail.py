# coding=utf-8
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import subprocess

host_server = 'smtp.163.com'
sender = 'aqszw818@163.com'
pwd = 'CHJGUPTKYVJCCDCD'
receiver = ['1065537421@qq.com',]
# receiver = '1326551344@qq.com'
mail_title = '灵犀系统'

def send_mail(mail_content):
    # open ssl
    smtp = SMTP_SSL(host_server)
    # 1: open，0: stop
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender, pwd)
    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender
    msg["To"] = ','.join(receiver)
    try:
        smtp.sendmail(sender, receiver, msg.as_string())
    except Exception:
        print('send mail fail!!!')
    else:
        print('send mail success!')
    finally:
        smtp.quit()

if __name__ == "__main__":
    #res = subprocess.call('ls -l', shell=True)
    #if not res:
    #    mail_content = 'execute success!'
    #else:
    #    mail_content = 'execute fail!!!!'
    mail_content = 'hello'
    send_mail(mail_content)