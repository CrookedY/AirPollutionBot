from apscheduler.schedulers.blocking import BlockingScheduler
from twitterbot import airnow

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes = 2)
def timed_job():
    airnow()

sched.start()
