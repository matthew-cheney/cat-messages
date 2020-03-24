import sqlite3
import datetime

def get_all_emails(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM emails")
    db_result = c.fetchall()
    conn.close()
    return db_result

def add_email(db_name, first_name, last_name, email):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM emails WHERE email=?", (email,))
    if c.fetchone() is not None:
        return "email already in use"
    params = (datetime.datetime.now(), first_name, last_name, email)
    c.execute("INSERT INTO emails VALUES (?,?,?,?)", params)
    conn.commit()
    conn.close()

# add_email('db/cat_emails.db', 'Skylie', 'Cheney', 'skyliecheney@gmail.com')
# res = get_all_emails('db/cat_emails.db')
# print(res)
