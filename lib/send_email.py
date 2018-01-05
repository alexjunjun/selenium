# coding=utf-8
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from lib.log_config import get_logger
from lib.read_config import readConfig
_mylogger = get_logger('bamboo')

mailto_list = readConfig('config.ini','email','mailto_list').replace(' ','').split(',') # 收件人列表
mail_host = readConfig('config.ini','email','mail_host') # 配置邮件服务器
mail_from = readConfig('config.ini','email','mail_from') #发件人
mail_pass = readConfig('config.ini','email','mail_pass') #密码
mail_postfix = readConfig('config.ini','email','mail_postfix') # 密码

def send_mail( sub, content, reportFile ):          # to_list：收件人；sub：主题；content：邮件内容
    msg = MIMEText(_text=content, _charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题

    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    part = MIMEText(open(reportFile, 'rb').read(), 'base64', 'utf-8')
    part["Content-Type"] = 'application/octet-stream'
    part["Content-Disposition"] = 'attachment; filename="%s"'%reportFile
    msg.attach(part) #添加附件

    msg['subject'] = Header(sub, 'utf-8')
    msg['From'] = mail_from
    msg['To'] = ','.join(mailto_list) #兼容多个收件人
    smtp = smtplib.SMTP()

    try:
        smtp.connect(mail_host)
        smtp.login(mail_from, mail_pass)
        smtp.sendmail(mail_from, mailto_list, msg.as_string())
        smtp.close()
        _mylogger.info('带附件测试报告发送成功！')
        return True
    except (Exception) as e:
        _mylogger.error(u'邮件发送失败：%s' %e)
        return False
if __name__ == '__main__':
    with open('../results/2017-09-13 14_55_20 test_result.html','r') as result:
        mail_body = result.read()
    email_result = send_mail(u"Aubb自动化测试结果",mail_body)
    if email_result:
        print (u"发送成功")
    else:
        _mylogger.error(email_result)
        print (u"发送失败")