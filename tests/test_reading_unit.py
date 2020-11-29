import unittest
from modules.Reading import Parameterizer, FileType

class TestReading(unittest.TestCase):

    def setUp(self):
        self.parameterizer = Parameterizer()

    def test_ffile_reading(self):
        params = self.parameterizer.get_parameters(FileType.F_file)
        self.assertEqual(params, {'fp': [0.01, 0.02, 0.05, 0.1], 'm': [1, 2], 'a': [1, 2]})

    def test_fbest_reading(self):
        params = self.parameterizer.get_parameters(FileType.Fbest_file)
        self.assertEqual(params, {"fp": 0.01, "m": 1, "a": 2})