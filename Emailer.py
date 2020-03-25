import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

import DBHandler
from CustomErrors import EmailNotFoundError
from get_cat import get_cat
from get_quote import get_quote


def send_verification_email(db_name, email):
    try:
        person = DBHandler.get_person_by_email_unverified(db_name, email)
    except EmailNotFoundError:
        return False

    verification_link = f'http://localhost:5000/verify/{person[3]}/{person[4]}'
    # verification_link = "http://www.realpython.com"
    subject = f"DailyCat Verification Email"
    html= f"""<html>
          <body>
          <p>Thank you for subscribing to DailyCat!<p>
          <p>To start receiving your daily dose of cute and cuddly cats, you must verify your email. Either click this link, or copy and paste it into your favorite browser:<br/>
          <a href="{verification_link}">{verification_link}</a></p>
          <p>If you did not subscribe to DailyCat, you may ignore this email.</p>
          </body>
          </html>"""

    with open('gmail_email.txt', 'r') as f:
        sender_email = f.read()
    with open('gmail_password.txt', 'r') as f:
        password = f.read()

    receiver_email = person[3]
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["Subject"] = subject
    message["To"] = receiver_email

    # Add body to email
    part1 = MIMEText(html, "html")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

    return True

def send_daily_cat(db_name, receiver_emails):
    get_cat()
    """people = []
    for receiver_email in receiver_emails:
        try:
            person = DBHandler.get_person_by_email_unverified(db_name, receiver_email)
            people.append(person)
        except EmailNotFoundError:
            continue"""

    subject = f"Cat of the Day - {datetime.datetime.today().strftime('%Y-%m-%d')}"
    quote = get_quote()

    html = f"""
    <html>
    <body>
    <p>{quote[0]}<br/>
    <i>{quote[1]}</i></p>
    <p><a href="localhost:5000/unsubscribe">Unsubscribe</a>
    </body>
    </html>
    """

    with open('gmail_email.txt', 'r') as f:
        sender_email = f.read()
    with open('gmail_password.txt', 'r') as f:
        password = f.read()

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(html, "html"))

    filename = 'daily_cat/cat.jpg'

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for receiver_email in receiver_emails:
            if receiver_email == '':
                continue
            message["To"] = receiver_email
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)

