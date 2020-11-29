import unittest
from modules.Calibration import ParameterTuning

class TestCalibration(unittest.TestCase):        

    def test_priority_logged_user(self):
       
        parameterTuning = ParameterTuning(1, "445566")
        self.assertIsNotNone(parameterTuning.loggedUser)

        with self.assertRaises(PermissionError) as context:
            parameterTuning = ParameterTuning(2, "sag_22311as")
        self.assertTrue("Sorry, user 2 is not allowed to perform calibrations on MultiMagNet.", context.exception)

    def test_calibration_integration(self):

        parameterTuning = ParameterTuning(1, "445566")
        self.assertEqual(parameterTuning.calibrate(250, False), True)
        