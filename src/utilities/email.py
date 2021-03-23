import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import base64

def send_email(sender, reciever, msg, subject, file_path=''):
    # For attach a file
    if file_path:
        # Read a file and encode it into base64 format
        fo = open(file_path, "rb")
        filecontent = fo.read()
        encodedcontent = base64.b64encode(filecontent)  # base64

    marker = "AUNIQUEMARKER"

    body = msg
    # Define the main headers.
    part1 = """From: From Person <%s>
    To: To Person <%s>
    Subject: %s
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary=%s
    --%s
    """ % (sender, reciever, subject, marker, marker)

    # Define the message action
    part2 = """Content-Type: text/plain
    Content-Transfer-Encoding:8bit

    %s
    --%s
    """ % (body, marker)

    # Define the attachment section
    if file_path:
        part3 = """Content-Type: multipart/mixed; name=\"%s\"
        Content-Transfer-Encoding:base64
        Content-Disposition: attachment; filename=%s

        %s
        --%s--
        """ % (os.path.basename(file_path), os.path.basename(file_path), encodedcontent, marker)

        message = part1 + part2 + part3
    else:
        message = part1 + part2

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, reciever, message)
        print("Successfully sent email")
    except Exception:
        print("Error: unable to send email")


USERNAME = "sexyscars555@gmail.com"
PASSWORD = 'rgqknpzhcesdvqqm'


# El atributo sender tiene que ser un email, porque sino el correo lo marcará como spam
def send_email_using_gmail(sender='Calandraca <sexyscars555@gmail.com>', receivers=None, text='', subject='', html=None):
    # assert isinstance(receivers, list)

    # login to my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  # default configuration
    server.starttls()  # secure connection
    server.ehlo()
    server.login(USERNAME, PASSWORD)

    # creating the msg
    smsg = f'Subject: {subject}\n\n{text}'

    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    if type(receivers) is list:
        msg['To'] = ','.join(receivers)
    else:
        msg['To'] = receivers
    msg['Subject'] = subject
    text_part = MIMEText(text, 'plain')
    msg.attach(text_part)
    if html:
        html_part = MIMEText(html, 'html')
        # Si existe html reemplazará al texto plano
        msg.attach(html_part)
    smsg = msg.as_string()

    server.sendmail(
        sender,
        receivers,
        smsg
    )
    print(f'The email to {receivers} has been send')
    server.quit()
    # with smtplib.SMTP() as server:
    # ...
    #  server.login()
    # ...
    # pass