#!/home/fred/dev/Quantum/.venv/bin/python3
# task_solver读取json文件，生成task_list, list中的每个元素是一个taskUnit对象
# TaskSolver类读取一个json文件，并返回一个task_list，其中每个元素是一个TaskUnit对象
import sys
from task_unit import TaskUnit
import json
import os
import re
from apscheduler.triggers.cron import CronTrigger
import importlib
if "/home/fred/dev/Quantum/" not in sys.path:
    sys.path.append("/home/fred/dev/Quantum/")
import service_api.event
from service_api.event import test_func_1, test_func_2

class TaskSolver(object):
    def __init__(self):
        self.json_file = None
        self.task_list = []
        self.module_list = [service_api.event,]

    def read_json(self, json_file: str) -> list[TaskUnit]:
        if os.path.exists(json_file) is False:
            raise FileNotFoundError("File not found")
        else:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                for task in data:
                    task_unit = TaskUnit(
                        task_name=task['task_name'],
                        func=self.func_solve(task),
                        trigger=self.trigger_solve(task)
                        )
                    self.task_list.append(task_unit)
        return self.task_list

    def trigger_solve(self, jsdata: dict) -> TaskUnit:
        """
        Resolve the trigger.
        FORMAT:
        hh:mm      : 18:31 stands for 18:31.
        TYPE:
        1-31. day of month
        41-47. week day
        
        """
    
        if jsdata["type"] in range(0, 32):
            if t := re.match(r'(\d{1,2}):(\d{2})', jsdata['time']):
                trigger = CronTrigger(
                    day_of_week='mon-fri',
                    hour=str(t.group(1)),
                    minute=str(t.group(2)),
                    timezone='Asia/Shanghai'
                    )
            else:
                trigger = None
        else:
            trigger = None
        return trigger
    
    def func_solve(self, task_dict: dict):
        func = None
        for mod in self.module_list:
            importlib.reload(mod)
            if task_dict['func'] in mod.__all__:
                func = eval(f"{mod.__name__}.{task_dict['func']}")
        return func

    def get_task_list(self):
        return self.task_list

