import schedule
from main import do_process
import time
from config import Config

schedule.every(Config.BOT_RUN_TIME).minutes.do(do_process)

while True:
    print("cron job is running")
    schedule.run_pending()
    time.sleep(1)
