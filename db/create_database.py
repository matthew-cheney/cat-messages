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

create_tables_string = """
CREATE TABLE emails (date_added text, first_name text, last_name text, email text)
"""

print('creating table(s)')
c.execute(create_tables_string)
conn.commit()

print('done')


