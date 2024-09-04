#!/home/fred/dev/Quantum/.venv/bin/python3

from apscheduler.triggers.cron import CronTrigger
import uuid

import random


class TaskUnit(object):
    def __init__(self, task_name: str, func, trigger: CronTrigger, timezong = 'Asia/Shanghai'):
        self.name = task_name
        self.uid = str(random.randint(1, 100000))
        self.func = func
        self.trigger = trigger
        if (self.trigger is None) or (self.func is None):
            self.name = None

    def __str__(self):
        return f"<{self.name}:{self.trigger}:{self.func}>"
    
