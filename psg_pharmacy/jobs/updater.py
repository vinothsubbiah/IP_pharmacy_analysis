from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api, 'cron', day_of_week='tue', hour=17, minute=49)
    #scheduler.add_job(schedule_api, 'interval', days=7)
    scheduler.start()