from abc import ABC, abstractmethod
from enum import Enum
import numpy as np
from random import uniform
from itertools import product
from Preprocessing import Image

class Metric(Enum):
    RE = 1
    JSD = 2

class ThresholdApproach(Enum):
    MTA = 1
    minTA = 2

class IMetric(ABC):
    """
    Metrics interface. The parameter 'is_adv' simulates a bigger metric value 
    for a given adversarial image, and a smaller metric value for a given legitimate image.
    """
    @abstractmethod
    def compute(self, image, reconstructed_image, is_adv = 0): raise NotImplementedError

class JSDMetric(IMetric):
    def compute(self, image, reconstructed_image, is_adv = 0): 
        if is_adv == 0: return uniform(0.001, 0.01)
        else: return uniform(0.02, 0.025)

class REMetric(IMetric):
    def compute(self, image, reconstructed_image, is_adv = 0):
        if is_adv == 0: return uniform(0.0025, 0.025)
        else: return uniform(0.025, 0.035)
        
class MetricComputation:
    """
    Computes the metric values of each defense component using only legitimate images.

    Parameters:
    --------------
    FP (list<double>): the false positive set;
    M (list<Metric>): a list containing the metric enumerations;
    A (list<ThresholdApproach>) a list containing the threshold approaches to be tested;
    images (list): the Vleg dataset containing only legitimate images;
    S_set (list): a list containing all the defense components.
    """
    def __init__(self, FP, M, A, images, S_set):
        self.__FP = FP
        self.__M = [Metric(m).name for m in M]
        self.__A = [ThresholdApproach(a).name for a in A]
        self.__vleg = images
        self.__sset = S_set
        self.__combinations = list(product(FP, M, A))
        self.__numCombinations = len(self.__combinations)
        self.__metrics = np.zeros(shape=(self.__numCombinations, len(S_set), len(images)))

    @staticmethod
    def get_metric(metric: Metric) -> IMetric:
        if metric == Metric.JSD: return JSDMetric()
        else: return REMetric()

    def __compute_metrics(self):        
        for i in range(self.__numCombinations):

            for j in range(len(self.__sset)):
                component = self.__sset[j]

                for k in range(len(self.__vleg)):
                    r_image = component.execute(self.__vleg[k])
                    
                    # computes the corresponding metric
                    self.__metrics[i][j][k] = MetricComputation.get_metric(self.__combinations[i][1]).compute(self.__vleg[k], r_image)

    def get_tau_set(self): 
        """
        Computes the threshold set "TAU" for each defense component. It contains 'c' times 'm' thresholds.

        Returns:
        --------------
        tau_set (np.ndarray): A 'c' x 'm' matrix. Each row corresponds to a combination, each cell to a component and each cell to a threshold.

        combinations (list): The list containing the parameter combinations.
        """
        import math
        tau_set = np.zeros(shape=(self.__numCombinations, len(self.__sset)))

        self.__compute_metrics()

        for i in range(self.__numCombinations): 
            for j in range(len(self.__sset)):
                metrics_desc_order = -np.sort(-self.__metrics[i][j]) # sorts in descending order
                index = math.ceil(self.__combinations[i][0] * len(metrics_desc_order))
                tau_set[i][j] = metrics_desc_order[index]
        
        return tau_set, self.__combinations