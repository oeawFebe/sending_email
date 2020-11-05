import codecs
import datetime
from email.mime.text import MIMEText
import os
import smtplib
import ssl
import sys
# To prevent encoding error.
sys.stdout=codecs.getwriter("utf-8")(sys.stdout)

def send_non_attachment_email():
    #______________variables______________
    gmail_address=os.environ.get("GMAILADDRESS")
    gmail_password=os.environ.get("GMAILPASSWORD")
    subject="auto_subject"
    body="""auto generated on {0}.<br>
        Please utilized dataframe with zip to send multiple email with different contents.<br>
        Also, formatting is very convenient""".format(datetime.date.today())
    mail_to=os.environ.get("GMAILADDRESS")

    msg=MIMEText(body,"html") # textmail is also possible
    msg["To"],msg['From'],msg["Subject"]=mail_to,gmail_address,subject
    server=smtplib.SMTP_SSL('smtp.gmail.com',465,context=ssl.create_default_context())
    server.login(gmail_address,gmail_password)
    server.send_message(msg)
    server.close()
    print("Testing for non-attachment email finished successfully.",file=sys.stderr)

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_attachment_email(filename):
    #_________variables_______________
    # filename='linalg_notes.pdf'
    gmail_address=os.environ.get("GMAILADDRESS")
    gmail_password=os.environ.get("GMAILPASSWORD")
    subject="auto_subject"
    body="""auto generated on {0}.<br>
        Please utilized dataframe with zip to send multiple email with different contents.<br>
        Also, formatting is very convenient""".format(datetime.date.today())
    mail_to=os.environ.get("GMAILADDRESS")

    msg2=MIMEMultipart()
    msg2["To"],msg2['From'],msg2["Subject"]=mail_to,gmail_address,subject
    msg2_text=MIMEText(body,"html")
    file=open(filename,'rb')
    attachment_file=MIMEBase("application",filename.split(".")[-1])
    attachment_file.set_payload((file).read())
    file.close()
    encoders.encode_base64(attachment_file)
    attachment_file.add_header("Content-Disposition","attachment",filename=filename)
    msg2.attach(attachment_file)
    server=smtplib.SMTP_SSL('smtp.gmail.com',465,context=ssl.create_default_context())
    server.login(gmail_address,gmail_password)
    server.send_message(msg2)
    server.close()
    print("Testing for pdf-attachment email finished successfully.",file=sys.stderr)
