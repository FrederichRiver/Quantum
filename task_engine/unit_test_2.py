# create unittest code
# test_task_manager.py

import unittest
from task_manager import AtomTask
from task_unit import TaskUnit
from apscheduler.triggers.cron import CronTrigger

def test_func_1():
    pass

def test_func_2():
    pass


class TestAtomTask(unittest.TestCase):
    def setUp(self):
        self.at = AtomTask()


    def test_add_task(self):
        task = TaskUnit('test_func_1', test_func_1,
                        CronTrigger(day_of_week='mon-fri', hour='18', minute='25', timezone='Asia/Shanghai')
                        )
        self.at.add_task(task)
        self.assertEqual(len(self.at.task_list), 1)
        self.assertEqual(self.at.task_list[0], task)

    def test_remove_task(self):
        task = TaskUnit('test_func_2', test_func_2,
                        CronTrigger(day_of_week='mon-fri', hour='18', minute='28', timezone='Asia/Shanghai')
                        )
        self.at.add_task(task)
        self.at.remove_task(task.uid)
        self.assertEqual(len(self.at.task_list), 0)
        self.assertEqual(len(self.at.task_id_map), 0)
    
    def test_remove_task_2(self):
        task = TaskUnit('test_func_1', test_func_1,
                        CronTrigger(day_of_week='mon-fri', hour='18', minute='28', timezone='Asia/Shanghai')
                        )
        self.at.add_task(task)
        self.at.remove_task(task.uid)
        self.assertEqual(len(self.at.task_list), 0)
        self.assertEqual(len(self.at.task_id_map), 0)
        self.at.remove_task(task.uid)
        self.assertEqual(len(self.at.task_list), 0)
        self.assertEqual(len(self.at.task_id_map), 0)
        self.at.print_jobs()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestAtomTask('test_add_task'))
    suite.addTest(TestAtomTask('test_remove_task'))
    suite.addTest(TestAtomTask('test_remove_task_2'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
