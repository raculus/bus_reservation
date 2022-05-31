from email import message
from email.mime import image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

f = open('gmail.txt', 'r')
text = f.read()
text = text.split('\n')

email = text[0]
email_pw = text[1]

def Send(subject, message, send_screenshot=False):

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if(send_screenshot):
        # 사진 첨부
        filename = 'Screenshot.png'
        attachment = open(filename, "rb").read()
        image = MIMEImage(attachment, name=filename)
        msg.attach(image)


    # Attach the attachment to the MIMEMultipart object
    # msg.attach(part)


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, email_pw)
    text = msg.as_string()
    server.sendmail(email, email, text)
    server.quit()

if __name__ == '__main__':
    Send('시작', '', True)