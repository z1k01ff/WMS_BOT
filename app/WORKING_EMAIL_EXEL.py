import smtplib
from email.message import EmailMessage

SENDER_LOGIN = 'berta/ntkach'
APP_PASSWORD = "Qwerty32"


subject = "BAYOYAYO BAYOYAYO"
SENDER_EMAIL = "ntkach@ub1.com.ua"
recipient_email = ['nsynovska@ub1.com.ua']
content = "NATALI PIPISYA"
excel_file = "/Users/admin/PycharmProjects/WMS_BOT/app/exel/soderzimoe_full_t.xlsx"
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = SENDER_EMAIL
msg['To'] = recipient_email
msg.set_content(content)

with open(excel_file, 'rb') as f:
    file_data = f.read()
msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=excel_file)

try:
    smtp = smtplib.SMTP('mail.berta.com.ua', 587)
except Exception as e:
    print(e)
    smtp = smtplib.SMTP_SSL('mail.berta.com.ua', 465)


smtp.login(SENDER_LOGIN, APP_PASSWORD)
smtp.send_message(msg)