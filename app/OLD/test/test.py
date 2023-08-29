import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


msg = MIMEMultipart()
msg['From'] = "ntkach@ub1.com.ua"
msg['To'] = "vchornyi@blyzenko.com.ua"
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = "subject"
msg.attach(MIMEText("text"))

part = MIMEBase('application', "octet-stream")
part.set_payload(open("app/exel/soderzimoe_full_t.xlsx", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="WorkBook3.xlsx"')
msg.attach(part)

#context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
#SSL connection only working on Python 3+

try:
    smtpObj = smtplib.SMTP('mail.berta.com.ua', 587)
except Exception as e:
    print(e)
    smtpObj = smtplib.SMTP_SSL('mail.berta.com.ua', 465)
#type(smtpObj)
smtpObj.ehlo()
# smtpObj.starttls()
smtpObj.login('berta/ntkach', "Qwerty32")
smtpObj.sendmail("ntkach@ub1.com.ua", "vchornyi@blyzenko.com.ua", msg.as_string()) # Or recipient@outlook



#
# smtp = smtplib.SMTP(server, port)
# if isTls:
#     smtp.starttls()
# smtp.login(username,password)
# smtp.sendmail(send_from, send_to, msg.as_string())
# smtp.quit()