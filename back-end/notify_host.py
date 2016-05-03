import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import os

def notify_host(recipients):
    fromaddr = os.environ["SENDEREMAIL"]
    # For testing purposes, I'm sending the email to myself
    toaddr = fromaddr
    msg = MIMEMultipart()

    msg["From"] = fromaddr
    msg["To"] = recipients
    msg["Subject"] = "cAterPI Client Order Received!"

    body = ("You have received a catering request from cAterPI.\n"
            "Please check the database and contact client for follow up")

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, os.environ["SENDEREMAILPW"])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
