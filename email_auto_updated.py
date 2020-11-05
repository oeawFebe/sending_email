import codecs,datetime,os,smtplib,ssl,sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
sys.stdout=codecs.getwriter("utf-8")(sys.stdout)# To prevent encoding error.


def send_gmail(mail_to,subject="",body="",attached_filename=None):
    gmail_address=os.environ.get("GMAILADDRESS")
    gmail_password=os.environ.get("GMAILPASSWORD")
    msg=MIMEMultipart() if attached_filename else MIMEText(body,"html")
    msg["To"],msg['From'],msg["Subject"]=mail_to,gmail_address,subject
    if attached_filename:
        msg_text=MIMEText(body,"html")
        with open(attached_filename,'rb') as f:
            attachment_file=MIMEBase("application",attached_filename.split(".")[-1])
            attachment_file.set_payload((f).read())
        encoders.encode_base64(attachment_file)
        attachment_file.add_header("Content-Disposition","attachment",filename=attached_filename)
        msg.attach(msg_text)
        msg.attach(attachment_file)

    server=smtplib.SMTP_SSL('smtp.gmail.com',465,context=ssl.create_default_context())
    server.login(gmail_address,gmail_password)
    server.send_message(msg)
    server.close()
    print("Finished sending email.",file=sys.stderr)
