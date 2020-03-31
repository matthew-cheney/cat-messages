import os

from server import app

"""from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

import DBHandler
import Emailer
db_name = 'db/cat_emails.db'
def daily_cat_trigger():
    all_emails = DBHandler.get_all_emails(db_name)
    Emailer.send_daily_cat(db_name, all_emails)

scheduler.configure(timezone='utc')
scheduler.add_job(daily_cat_trigger, 'interval', seconds=60)
scheduler.start()
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
"""
app.run(debug=True, host='0.0.0.0', port=5000)
