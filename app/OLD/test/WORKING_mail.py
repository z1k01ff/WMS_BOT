import smtplib
import time

#SPOSIB 1
FROM = "ntkach@ub1.com.ua"
SUBJECT = "zdarova"
TEXT = "Vladik pisyun"
TO = ["vchornyi@blyzenko.com.ua"] # must be a list

message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)


#SPOSIB 2
body = 'Subject: Subject Here .\nDear ContactName, \n\n' + 'Email\'s BODY text' + '\nYour :: Signature/Innitials'
try:
    smtpObj = smtplib.SMTP('mail.berta.com.ua', 587)
except Exception as e:
    print(e)
    smtpObj = smtplib.SMTP_SSL('mail.berta.com.ua', 465)
#type(smtpObj)
smtpObj.ehlo()
# smtpObj.starttls()
smtpObj.login('berta/ntkach', "Qwerty32")
for n in range(10):
    smtpObj.sendmail(FROM, TO, message) # Or recipient@outlook
    time.sleep(10)

smtpObj.quit()
