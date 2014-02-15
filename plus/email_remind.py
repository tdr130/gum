#
#   email_remind.py - remind plugin
#       and null
#
'''
gum_emailremind = {
    'mail_host':'smtp.126.com',
    'mail_user':'user',
    'mail_pass':'pass',
    'mail_postfix':'126.com',
    'tolist':['user@a.com', 'admin@b.com'],
    'sub':'主题',
    'text':'内容'
}
from plus.email_remind import send_mail
send_mail(gum_emailremind)
'''
import smtplib
from email.mime.text import MIMEText

def send_mail(mails):
    me = mails['mail_user'] + '<' + mails['mail_user'] + '@' + mails['mail_postfix'] + '>'
    msg = MIMEText(mails['text'])
    msg['Subject'] = mails['sub']
    msg['From'] = me
    msg['To'] = ';'.join(mails['tolist'])
    try:
        smail = smtplib.SMTP()
        smail.connect(mails['mail_host'])
        smail.login(mails['mail_user'], mails['mail_pass'])
        smail.sendmail(me, mails['tolist'], msg.as_string())
        smail.close()
        return True
    except Execption, e:
        print str(e)
        return False
