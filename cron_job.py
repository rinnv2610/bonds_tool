import schedule
from main import do_process
import time

schedule.every(10).minutes.do(do_process)

while True:
    print("cron job is running")
    schedule.run_pending()
    time.sleep(1)
