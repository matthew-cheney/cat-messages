import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from get_cat import get_cat
from get_quote import get_quote
from glob import glob
from datetime import datetime

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

with open('gmail_email.txt', 'r') as f:
    sender_email = f.read()
with open('recipient_emails.txt', 'r') as f:
    receiver_emails = f.read().split('\n')
# password = input("Type your password and press enter:")
with open('gmail_password.txt', 'r') as f:
    password = f.read()

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "html"))

get_cat()

cat_filenames = glob('cat_images/cat_*')

filename = f"cat_images/cat_{len(cat_filenames) - 1:05d}.jpg"  # In same directory as script

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
