# -*- coding: utf-8 -*-
# @Time    : 2018/10/4 1:16 PM
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys

sys.path.append('./')

import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from db.db_manager import DatabaseManager
from config import mail_host, mail_user, mail_pass


def send_email(chs_name, receiver, username, password, port, admin_open_port, node_name_list):
    sender = 'piaozhx@shanghaitech.edu.cn'
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_content = '''
    Hi, %s:
目前AI集群主存储已即将用完(78T/80T), 由于整套系统是部署到主存储上, 因而满载会出现各种异常问题. 
加上最近集群人数越来越多, 故最近开始限制大家在主存储上的使用量(限制1人1T), /p300下是新存储, 实在有很多文件的人可以往上面放

下周一(2019年5月20日)开始实际限制主存储上的使用, 所有使用量超限的用户将冻结账号

好的使用习惯:
1. 所有的网络模型数据在一次训练完后只留最好的和最近的, 删除无意义的临时模型
2. 多人协作大数据集时, 共享数据集而不是一个一个
3. 结束一个项目之后及时把不需要的临时文件删除, 整理文档, 不要到半年之后自己都忘记这个文件有没有用, 不敢删

AI集群运维团队
    ''' % (chs_name)

    message = MIMEText(mail_content, 'plain', 'utf-8')
    message['From'] = Header("AI集群管理", 'utf-8')
    message['To'] = Header("AI集群用户", 'utf-8')

    message['Subject'] = Header('AI集群管理系统升级', 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)  # 25 为 SMTP 端口号

        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()

        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("%s 邮件发送成功" % receiver)
        return True

    except smtplib.SMTPException:
        print("Error: %s 无法发送邮件" % receiver)
        return False


def main():
    db = DatabaseManager()
    user_info_list = db.get_all_user_info() + db.get_cs280_user_info()

    count = 0
    for user_info in user_info_list:
        username = user_info['username']
        chs_name = user_info['chinese_name']
        receiver = user_info['email']
        container_port = user_info['container_port']
        open_port_range = user_info['open_port_range']

        if receiver in ['test', 'test2', 'NA']:
            continue

        node_name_list = [p['name'] for p in user_info['permission']]
        success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)

        while not success:
            # count = 0
            time.sleep(10)
            success = send_email(chs_name, receiver, username, 'plus', container_port, open_port_range, node_name_list)

        # count += 1
        #
        # if count == 5:
        #     count = 0
        #     time.sleep(10)


if __name__ == '__main__':
    main()
