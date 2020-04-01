import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

from dailycat.settings import SENDER_EMAIL, EMAIL_PASSWORD
from dailycat.utils import DBHandler
from dailycat.errors.CustomErrors import EmailNotFoundError
from daily_cat_email import get_cat
from daily_cat_email import get_quote


def send_verification_email(db_name, email):
    try:
        person = DBHandler.get_person_by_email_unverified(db_name, email)
    except EmailNotFoundError:
        return False

    verification_link = f'https://www.cheneycreations.com/daily-cat/verify/{person[3]}/{person[4]}'
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

    receiver_email = person[3]
    message = MIMEMultipart("alternative")
    message["From"] = SENDER_EMAIL
    message["Subject"] = subject
    message["To"] = receiver_email

    # Add body to email
    part1 = MIMEText(html, "html")

    message.attach(part1)

    context = ssl.create_default_context()


    s = smtplib.SMTP('cheneycreations.com')
    s.ehlo()
    s.login(SENDER_EMAIL, EMAIL_PASSWORD)
    s.login(SENDER_EMAIL, EMAIL_PASSWORD)
    text = message.as_string()
    s.sendmail(SENDER_EMAIL, receiver_email, text)
    s.quit()
    print(f'sent confirmation email to {receiver_email}')
    return True

def send_daily_cat(db_name, receiver_emails):
    dirname = os.path.dirname(__file__)

    DB_NAME = os.path.join(dirname, 'db/cat_emails.db')

    subject = f"Cat of the Day - {datetime.datetime.today().strftime('%Y-%m-%d')}"

    quote = get_quote()

    body = f"""
    <html>
    <body>
    <p>{quote[0]}<br/>
    <i>{quote[1]}</i></p>
    </body>
    </html>
    """

    # with open('gmail_email.txt', 'r') as f:
    #     sender_email = f.read()
    # password = input("Type your password and press enter:")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "html"))

    filename = get_cat()

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

    s = smtplib.SMTP('cheneycreations.com')
    s.ehlo()
    s.login(SENDER_EMAIL, EMAIL_PASSWORD)
    for receiver_email in receiver_emails:
        if receiver_email == '':
            continue
        message["To"] = receiver_email
        text = message.as_string()
        s.sendmail(SENDER_EMAIL, receiver_email, text)
    s.quit()
