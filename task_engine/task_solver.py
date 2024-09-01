# task_solver读取json文件，生成task_list, list中的每个元素是一个taskUnit对象
# TaskSolver类读取一个json文件，并返回一个task_list，其中每个元素是一个TaskUnit对象
from task_unit import TaskUnit
import json
import os
import re
from apscheduler.triggers.cron import CronTrigger

class TaskSolver(object):
    def __init__(self):
        self.json_file = None
        self.task_list = []

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
        for k in jsdata.keys():
            if k["type"] in range(1, 32):
                if t := re.match(r'(\d{1,2}):(\d{2})', jsdata['time']):
                    trigger = CronTrigger(
                        day_of_week='mon-fri',
                        hour=int(t.group(1)),
                        minute=int(t.group(2)),
                        timezone=self.timezone)
                else:
                    trigger = None
            else:
                trigger = None
        return trigger
    
    def func_solve(self, task_dict: dict) -> function:
        func = None
        for mod in self.module_list:
            importlib.reload(mod)
            for func in mod.__all__:
                self.func_list[func] = eval(f"{mod.__name__}.{func}")
        return 1
        return func

    def get_task_list(self):
        return self.task_list

