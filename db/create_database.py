import sqlite3
import sys
import os

DEFAULT_DB_FILENAME = 'cat_emails.db'

if len(sys.argv) > 1:
    print(f'loading db_filename: {sys.argv[1]}')
    db_filename = sys.argv[1]
else:
    print(f'using default db_filename: {DEFAULT_DB_FILENAME}')
    db_filename = DEFAULT_DB_FILENAME

if os.path.exists(db_filename):
    print(f'{db_filename} already exists')
    exit(1)

print(f'establishing connections to {db_filename}')
conn = sqlite3.connect(db_filename)
c = conn.cursor()

print('creating table(s)')
c.execute("CREATE TABLE emails (date_added text, first_name text, last_name text, email text)")
c.execute("CREATE TABLE unverified_emails (date_added text, first_name text, last_name text, email text, verify_key text)")

conn.commit()

print('done')


