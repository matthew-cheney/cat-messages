import DBHandler
import Emailer
db_name = 'db/cat_emails.db'
all_emails = DBHandler.get_all_emails(db_name)
Emailer.send_daily_cat(db_name, all_emails)
