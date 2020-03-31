import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

from daily_cat_email.get_cat import get_cat
from daily_cat_email.get_quote import get_quote
from dailycat import utils
from daily_cat_email.settings import *

import os
dirname = os.path.dirname(__file__)

# DB_NAME = os.path.join(dirname, 'db/cat_emails.db')

subject = f"Cat of the Day - {datetime.today().strftime('%Y-%m-%d')}"

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
receiver_emails = utils.DBHandler.get_all_emails(DB_PATH)
# password = input("Type your password and press enter:")
password = EMAIL_PASSWORD

sender_email = 'matthew@cheneycreations.com'

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
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
s.login(sender_email, password)
for receiver_email in receiver_emails:
    if receiver_email == '':
        continue
    message["To"] = receiver_email
    text = message.as_string()
    s.sendmail(sender_email, receiver_email, text)
s.quit()
