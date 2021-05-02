import unittest



import luigi
import pytest
from luigi import Task, Parameter

class InstanceTest(unittest.TestCase):
    def test_fundamental(self):
        return client.post('/fundamental', data=dict(
            ticker="AAPL",
            model="GGM",
            years=5,
            rate=0.04,
            growth=0.02
        ), follow_redirects=True)



class InstanceTest(unittest.TestCase):

    def test_simple(self):
        class DummyTask(Task):
            x = Parameter()

        dummy_1 = DummyTask(1)
        dummy_2 = DummyTask(2)
        dummy_1b = DummyTask(1)

        self.assertNotEqual(dummy_1, dummy_2)
        self.assertEqual(dummy_1, dummy_1b)

    def test_direct_python(self):
        t = luigi.LocalTarget(is_tmp=True)
        args = ['python', 'tasks/tasks.py', 'GetDividends', '--tiker', "AAPL", '--local-scheduler', '--no-lock']
        self._run_cmdline(args)
        self.assertTrue(t.exists())

if __name__ == '__main__':
    unittest.main()
