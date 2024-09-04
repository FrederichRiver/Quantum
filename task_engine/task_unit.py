#!/home/fred/dev/Quantum/.venv/bin/python3

from apscheduler.triggers.cron import CronTrigger
import uuid




class TaskUnit(object):
    def __init__(self, task_name: str, func, trigger: CronTrigger, timezong = 'Asia/Shanghai'):
        self.name = task_name
        self.uid = uuid.uuid4()
        self.func = func
        self.trigger = trigger
        if (self.trigger is None) or (self.func is None):
            self.name = None

    def __str__(self):
        return f"<{self.name}:{self.flag}:{self.trigger}>"
    
