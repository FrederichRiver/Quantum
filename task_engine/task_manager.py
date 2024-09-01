# AtomTask是基于APScheduler构建的类

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.job import Job
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.base import BaseExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from typing import List, Dict, Any, Union, Optional
from datetime import datetime
import logging
import os
import time
import json
import copy
import traceback
import threading
import asyncio
import uuid
import random
import string
import sys
import re
import pytz
import uuid
import task_unit


class AtomTask(BackgroundScheduler):
    def __init__(self, scheduler: BaseScheduler, job_store: SQLAlchemyJobStore, executor: ThreadPoolExecutor):
        self.scheduler = scheduler
        self.job_store = job_store
        self.executor = executor
        self.task_map = {}  # task_id -> AtomTask
        self.task_id_map = {}  # task_id -> job_id
        self.job_id_map = {}  # job_id -> task_id
        self.job_id_task_id_map = {}

    def add_task(self, task: TaskUnit):
        self.task_map[task.task_id] = task
        self.task_id_map[task.task_id] = None
        self.job_id_map[task.job_id] = task.task_id

    def remove_task(self, task_id: str):
        task = self.task_map.get(task_id)
        if task:
            self.task_map.pop(task_id)
            self.task_id_map.pop(task_id)
            self.job_id_map.pop(task.job_id)
        
    def get_task(self, task_id: str):
        return self.task_map.get(task_id)
    
    def get_task_id(self, job_id: str):
        return self.job_id_map.get(job_id)
    
    def run(self):
        self.scheduler.start()
    
