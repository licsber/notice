from email.mime.text import MIMEText
from email.header import Header
import smtplib


class SMTP:
    def __init__(self, password, sender='silverwings233@qq.com', smtp_server='smtp.qq.com',
                 username='silverwings233@qq.com'):
        self.sender = sender
        self.smtp = smtplib.SMTP()

        self.smtp.connect(smtp_server)
        self.smtp.login(username, password)

    def send_mail_to(self, title, body, receiver='silverwings233@qq.com', mail_from='Licsber Automatic'):
        message = MIMEText(body, 'plain', 'utf-8')
        message["Accept-Language"] = "zh-CN"
        message["Accept-Charset"] = "ISO-8859-1,utf-8"
        message['From'] = mail_from
        message['To'] = receiver
        message['Subject'] = Header(title, 'utf-8')

        try:
            self.smtp.sendmail(self.sender, receiver, message.as_string())
            return True
        except smtplib.SMTPException:
            return False
