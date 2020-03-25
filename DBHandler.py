import sqlite3
import datetime

from CustomErrors import EmailNotFoundError


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

def get_all_unverified_emails(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM unverified_emails")
    db_result = c.fetchall()
    conn.close()
    return db_result

def get_all_emails(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM emails")
    db_result = c.fetchall()
    conn.close()
    return [x[3] for x in db_result]

def add_unverified_email(db_name, first_name, last_name, email, verify_key):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM unverified_emails WHERE email=?", (email,))
    if c.fetchone() is not None:
        return "email already in use"
    params = (datetime.datetime.now(), first_name, last_name, email, verify_key)
    c.execute("INSERT INTO unverified_emails VALUES (?,?,?,?,?)", params)
    conn.commit()
    conn.close()

def get_person_by_email_unverified(db_name, email):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM unverified_emails WHERE email=?", (email,))
    res = c.fetchone()
    if res is None:
        raise EmailNotFoundError('email not found in unverified_emails')
    return res

def verify_email(db_name, email):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM unverified_emails WHERE email=?", (email,))
        try:
            date_added, first_name, last_name, email, verify_key = c.fetchone()
            c.execute("DELETE FROM unverified_emails WHERE email=?", (email,))
            c.execute("INSERT INTO emails VALUES (?,?,?,?)",
                      (datetime.datetime.now(), first_name, last_name, email))
            conn.commit()
        except TypeError:
            # Email not found
            raise EmailNotFoundError(f'{email} not found in unverified_emails table')
    finally:
        conn.close()

def remove_email(db_name, email):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("DELETE FROM emails WHERE email=?",
                  (email,))
        conn.commit()
    finally:
        conn.close()

# add_email('db/cat_emails.db', 'Skylie', 'Cheney', 'skyliecheney@gmail.com')
# res = get_all_emails('db/cat_emails.db')
# print(res)
