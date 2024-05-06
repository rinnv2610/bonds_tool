import schedule
from main import do_process, clear_memory
import time
from config import Config

# Schedule notify bond to tele
schedule.every(int(Config.BOT_RUN_TIME)).minutes.do(do_process)

# Schedule memory clearing task
schedule.every().day.at("00:00").do(clear_memory)

while True:
    print("cron job is running")
    schedule.run_pending()
    time.sleep(1)
