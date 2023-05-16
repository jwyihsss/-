#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from utils import config
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class MailSender:
    """邮件发送方法"""

    def __init__(self):
        self.sender = config.email.sender_email
        self.password = config.email.password
        self.smtp_server = config.email.smtp_server
        self.receiver = config.email.receiver_email

    def send_email(self, subject, body, attachment=None):
        """构造邮件信息"""

        msg = MIMEText(body, _subtype='plain', _charset='utf-8')
        msg['From'] = self.sender
        msg['To'] = ";".join(self.receiver)
        msg['Subject'] = subject
        server = smtplib.SMTP()

        # 添加附件
        if attachment is not None:
            with open(attachment, 'rb') as f:
                attachment_file = MIMEApplication(f.read(), _subtype='txt')
                attachment_file.add_header('content-disposition', 'attachment', filename=attachment.split('/')[-1])
                msg.attach(attachment_file)

        server.connect(self.smtp_server)
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.receiver, msg.as_string())
        server.quit()


if __name__ == '__main__':
    mail = MailSender()
    mail.send_email(
        subject='接口自动化错误报告',
        body='error'
    )
