# 定义task类，它可以基于参数生成，也可以通过读取json文件生成
# 其属性包括:task_name, id, task_func, trigger
import uuid
from apscheduler.triggers import trigger

class taskUnit(object):
    def __init__(self, task_name: str, func: function, trigger: trigger):
        self.name = task_name
        self.uid = uuid.uuid4()
        self.func = func
        self.trigger = trigger
        if (self.trigger is None) or (self.func is None):
            self.name = None

    def __str__(self):
        return f"<{self.name}:{self.flag}:{self.trigger}>"
    
