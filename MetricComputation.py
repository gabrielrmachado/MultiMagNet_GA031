from abc import ABC, abstractmethod
from enum import Enum
import numpy as np
from random import uniform
from itertools import product

class Metric(Enum):
    RE = 1
    JSD = 2

class ThresholdApproach(Enum):
    MTA = 1
    minTA = 2

class IMetric(ABC):
    @abstractmethod
    def compute(self, image, reconstructed_image): raise NotImplementedError

class JSDMetric(IMetric):
    def compute(self, image, reconstructed_image):
        return uniform(0.001, 0.01)

class REMetric(IMetric):
    def compute(self, image, reconstructed_image):
        return uniform(0.0025, 0.025)

class MetricComputation:
    """
    Computes the metric values of each defense component using only legitimate images.

    Parameters:
    --------------
    FP (list<double>): the false positive set;
    M (list<Metric>): a list with the metrics enumerations;
    A (list<ThresholdApproach>) a list with threshold approaches to be tested;
    Vleg_dataset (list): the Vleg dataset containing only legitimate images;
    S_set (list): a list containing all the defense components.
    """
    def __init__(self, FP, M, A, Vleg_dataset, S_set):
        self.__FP = FP
        self.__M = M
        self.__A = A
        self.__vleg = Vleg_dataset
        self.__sset = S_set
        self.__combinations = list(product(FP, M, A))
        self.__numCombinations = len(self.__combinations)
        self.__metrics = np.zeros(shape=(self.__numCombinations, len(S_set), len(Vleg_dataset)))

    def __get_metric(self, metric: Metric) -> IMetric:
        if metric == Metric.JSD: return JSDMetric()
        else: return REMetric()

    def compute_metrics(self):
        from Helper import Helper
        
        for i in range(self.__numCombinations):

            for j in range(len(self.__sset)):
                component = self.__sset[j]

                for k in range(len(self.__vleg)):
                    r_image = component.execute(self.__vleg[k])
                    self.__metrics[i][j][k] = self.__get_metric(self.__combinations[i][1]).compute(self.__vleg[k], r_image)

        print(self.__metrics, self.__metrics.shape)

    def get_tau_set(self):
        pass


# from Data import ImageDAO, Dataset, AttackAlgorithm
# from Components import Factory, Component

# f = Component()
# m = MetricComputation([0.1, 0.2, 0.3, 0.25], [Metric.RE, Metric.JSD], [ThresholdApproach.MTA], ImageDAO.get_images(100)[0], [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)])
# m.compute_metrics()


# from Data import ImageDAO, Dataset, AttackAlgorithm

# i, l = ImageDAO.get_images(255, Dataset.Training)
# print(len(i), len(l))

# iadv, ladv = ImageDAO.get_Vdataset(i, l, AttackAlgorithm.FGSM, eps=0.3)
# print(len(iadv), len(ladv))