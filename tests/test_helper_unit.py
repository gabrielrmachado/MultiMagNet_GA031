import unittest
from modules.Helper import Helper
from modules.Components import Factory, Component
from modules.MetricComputation import ThresholdApproach

class TestHelper(unittest.TestCase):

    def test_get_ensemble(self):
        f = Component()
        sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
            f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

        idx, _ = Helper.getEnsembleMembers(sset, 3)
        self.assertEqual(len(idx), 3)
         
        with self.assertRaises(ArithmeticError) as context:
            idx, _ = Helper.getEnsembleMembers(sset, 4)
        self.assertTrue("Number of members must be odd.", context.exception)

        with self.assertRaises(AttributeError) as context:
            idx, _ = Helper.getEnsembleMembers(sset, 0)
        self.assertTrue("Invalid number.", context.exception)

        with self.assertRaises(AttributeError) as context:
            idx, _ = Helper.getEnsembleMembers(sset, len(sset)+1)
        self.assertTrue("Invalid number.", context.exception)

    def test_threshold_approach(self):
        metrics = [0.002, 0.025, 0.044, 0.0015, 0.001]
        metrics_approach = Helper.apply_threshold_approach(metrics, ThresholdApproach.MTA.value)
        self.assertCountEqual(metrics, metrics_approach)

        metrics_approach = Helper.apply_threshold_approach(metrics, ThresholdApproach.minTA.value)
        self.assertCountEqual(metrics_approach, [0.001, 0.001, 0.001, 0.001, 0.001])
