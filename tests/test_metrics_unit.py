import unittest
from modules.MetricComputation import MetricComputation, Metric, ThresholdApproach

class TestMetrics(unittest.TestCase):

    def setUp(self):
        from modules.Data import ImageDAO
        from modules.Components import Component, Factory

        f = Component()
        self.fp = [0.01, 0.05, 0.1]
        self.metrics = [Metric.JSD, Metric.RE]
        self.a = [ThresholdApproach.minTA, ThresholdApproach.MTA]
        self.images_vleg, _ = ImageDAO.get_images(10)
        self.m = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

        self.computation = MetricComputation(self.fp, self.metrics, self.a, self.images_vleg, self.m)

    def test_size_tau_set(self):
        tau_set, _ = self.computation.get_tau_set()
        self.assertEqual(tau_set.flatten().shape[0], len(self.fp) * len(self.metrics) * len(self.a) * len(self.m))

    def test_size_combinations(self):
        _, combinations = self.computation.get_tau_set()
        self.assertEqual(len(combinations), len(self.fp) * len(self.metrics) * len(self.a))

    def test_computation_index_k(self):
        import numpy as np
        import math

        metrics = self.computation.compute_metrics()
        tau_set, combinations = self.computation.get_tau_set()

        for i in range(len(combinations)): 
            for j in range(len(self.m)):
                metrics_desc_order = -np.sort(-metrics[i][j]) # sorts in descending order
                index = math.ceil(combinations[i][0] * len(metrics_desc_order))
                self.assertEqual(tau_set[i][j], metrics_desc_order[index])


