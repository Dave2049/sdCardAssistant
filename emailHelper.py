import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket

def sendMail(Subject, body):
    print("startSendMail")
    try:
        fromaddr = "GetSdCardScript@gmail.com"
        toaddr ="monitoring.2049@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = Subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "Python_Beste")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except socket.gaierror:
        print('socketError')
        raise Exception
