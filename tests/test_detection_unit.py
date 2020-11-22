import unittest
from modules.Detection import Detection

class TestDetection(unittest.TestCase):

    def test_count_votes(self):
        vm = [0.01, 0.01425, 0.002135, 0.001145, 0.075]
        tb = [0.005, 0.0035, 0.004, 0.007, 0.0105]
        self.assertEqual(Detection(vm, tb).detect(), False)

        vm = [0.01, 0.01425, 0.04, 0.001145, 0.075]
        tb = [0.05, 0.035, 0.04, 0.007, 0.0105]
        self.assertEqual(Detection(vm, tb).detect(), True)
