# create unittest code
# test_task_solver.py
import unittest
from task_solver import TaskSolver
from task_unit import TaskUnit
from apscheduler.triggers.cron import CronTrigger
from service_api import event

class TestTaskSolver(unittest.TestCase):
    def setUp(self):
        self.ts = TaskSolver()
        self.ts.json_file = '/home/fred/dev/Quantum/task_engine/test.json'
        self.ts.read_json(self.ts.json_file)

    def test_read_json(self):
        self.assertEqual(len(self.ts.task_list), 2)
        self.assertIsInstance(self.ts.task_list[0], TaskUnit)
        self.assertIsInstance(self.ts.task_list[0].trigger, CronTrigger)

    def test_trigger_solve(self):
        jsdata = {
            "task_name": "test_func_1",
            "func": "test_func_1",
            "time": "18:31",
            "type": 0
        }
        self.assertIsInstance(self.ts.trigger_solve(jsdata), CronTrigger)

    def test_func_solve(self):
        jsdata = {
            "task_name": "test_func_1",
            "func": "test_func_1",
            "time": "18:31",
            "type": 0
        }
        self.assertEqual(self.ts.func_solve(jsdata), event.test_func_1)

    def test_get_task_list(self):
        self.assertEqual(self.ts.get_task_list(), self.ts.task_list)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestTaskSolver('test_read_json'))
    suite.addTest(TestTaskSolver('test_trigger_solve'))
    suite.addTest(TestTaskSolver('test_func_solve'))
    suite.addTest(TestTaskSolver('test_get_task_list'))
    runner = unittest.TextTestRunner()
    runner.run(suite)



