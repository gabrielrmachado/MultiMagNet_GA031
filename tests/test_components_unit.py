import unittest
from modules.Components import Factory, Repository
from modules.MetricComputation import ThresholdApproach

class TestComponents(unittest.TestCase):

    def test_get_ensemble(self):
        r = Repository()
        sset = r.getSSet()

        idx, _ = r.getEnsembleMembers(3)
        self.assertEqual(len(idx), 3)
         
        with self.assertRaises(ArithmeticError) as context:
            idx, _ = r.getEnsembleMembers(4)
        self.assertTrue("Number of members must be odd.", context.exception)

        with self.assertRaises(AttributeError) as context:
            idx, _ = r.getEnsembleMembers(0)
        self.assertTrue("Invalid number.", context.exception)

        with self.assertRaises(AttributeError) as context:
            idx, _ = r.getEnsembleMembers(len(sset)+1)
        self.assertTrue("Invalid number.", context.exception)

