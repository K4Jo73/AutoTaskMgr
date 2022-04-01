import sys
import os
import atm_logger as audit
import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("script name is " + __name__)
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "k4jo73@gmail.com"
password = os.environ.get('PythonGMailPwd')
defaultMailSubject = "Auto Task Manager Alert"
MailMessageIntro = "This message was sent by Auto Task Manager"
MailMessageOutro = "Thanks"

def yes_or_no(question, default_no=True):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    choices = ' [y/N]: ' if default_no else ' [Y/n]: '
    default_answer = 'n' if default_no else 'y'
    reply = str(input(question + choices)).lower().strip() or default_answer
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False if default_no else True



def send_Mail(receiver_email,message,subject=defaultMailSubject):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    # sender_email = "k4jo73@gmail.com"
    # receiver_email = "k4jo73@outlook.com"
    # smtp_server = "smtp.gmail.com"
    # port = 587  # For starttls
    password = input("Type your password and press enter: ")
    # password = os.environ.get('PythonGMailPwd')

    msgTxt = MailMessageIntro+"\n\n"+message+"\n\n"+MailMessageIntro
    msgHTML = MailMessageIntro+"<BR/><BR/>"+message+"<BR/><BR/>"+MailMessageIntro
    part1 = MIMEText(msgTxt, 'plain')
    part2 = MIMEText(msgHTML, 'html')
    audit.logging.info("Preparing mail to send from "+sender_email+" to "+receiver_email)
    # msg = EmailMessage()
    msg = MIMEMultipart('alternative')
    # msg.set_content(MailMessageIntro+message+MailMessageIntro)
    msg.attach(part1)
    msg.attach(part2)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    audit.logging.debug("Message Object Content: "+str(msg))

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        audit.logging.info("\tSending email")
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
    except Exception as err:
        audit.logging.info("\tSending failed!")
        audit.logging.error(sys._getframe().f_code.co_name + f" - From "+sender_email+" to "+receiver_email+" - Unexpected {err=}, {type(err)=}")
    finally:
        audit.logging.info("\tMessage sent")
        server.quit() 