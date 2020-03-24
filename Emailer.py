import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import DBHandler
from CustomErrors import EmailNotFoundError


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

def send_cat(db_name, receiver_emails):
    people = []
    for receiver_email in receiver_emails:
        try:
            person = DBHandler.get_person_by_email_unverified(db_name, receiver_email)
            people.append(person)
        except EmailNotFoundError:
            continue

    verification_link = f'http://localhost:5000/verify/{person[3]}/{person[4]}'
    # verification_link = "http://www.realpython.com"
    subject = f"DailyCat Verification Email"
    html = f"""<html>
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
    with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                          context=context) as server:
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

    return True