from abc import ABC, abstractmethod

class IMetric(ABC):
    @abstractmethod
    def compute(self): raise NotImplementedError

class JSDMetric(IMetric):
    def compute(self):
        pass

class REMetric(IMetric):
    def compute(self):
        pass

class MetricComputation:
     def __init__(self, metric):
        if isinstance(metric, IMetric) == False:
            raise TypeError("metric object does not implement IMetric interface.")
        self.__metric = metric