class ParameterTuning:
    pass

from Data import ImageDAO, Dataset, AttackAlgorithm
from Components import Factory, Component
from MetricComputation import Metric, MetricComputation, ThresholdApproach
from Evaluation import Assessment

f = Component()

sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
    f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

m = MetricComputation([0.01, 0.02, 0.05, 0.1], [Metric.RE, Metric.JSD], [ThresholdApproach.MTA, ThresholdApproach.minTA], ImageDAO.get_images(100)[0], sset)

tau_set, combinations = m.get_tau_set()
vdata, vlabels = ImageDAO.get_Vdataset(200, AttackAlgorithm.FGSM, eps=0.3)
a = Assessment(vdata, vlabels, tau_set, sset, combinations)
a.evaluate(m)