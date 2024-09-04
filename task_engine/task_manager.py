# AtomTask是基于APScheduler构建的类

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from task_unit import TaskUnit



class AtomTask(BackgroundScheduler):
    def __init__(self):
        super(AtomTask, self).__init__(timezone='Asia/Shanghai')
        self.job_stores =  {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        self.executors = {
            'default': ThreadPoolExecutor(5),
            'processpool': ProcessPoolExecutor(5)
        }
        self.task_list = []
        self.task_id_map = []

    def add_task(self, task: TaskUnit):
        if task.uid not in self.task_id_map:
            self.task_list.append(task)
            self.task_id_map.append(task.uid)
            self.add_job(task.func, trigger=task.trigger, id=task.uid, name=task.name, jobstore='default', executor='default', replace_existing=True)

    def remove_task(self, task_id):
        """
        Remove a task from the task list by task id.
        """
        for task in self.task_list:
            if task.uid == task_id:
                self.remove_job(task_id)
                self.task_list.remove(task)
                self.task_id_map.remove(task_id)
                break

    
    def run(self):
        self.start()
    
