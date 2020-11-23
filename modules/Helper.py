import random
import numpy as np
from MetricComputation import ThresholdApproach

class Helper:
    @staticmethod
    def getEnsembleMembers(S_set, numMembers: int):
        """
        Receives the S set and choose randomly an odd number of members.

        Returns:
        --------------

        indexes (list): a list with the corresponding chosen indexes in S set;
        components (list): a list containing the corresponding components, represented by the 'indexes' list.
        """

        if numMembers < 1 or numMembers > len(S_set):
            raise AttributeError("Invalid number.")
        elif numMembers % 2 == 0:
            raise ArithmeticError("Number of members must be odd.")
       

        values = random.sample(list(enumerate(S_set)), numMembers)        
        indexes = []
        components = []
        
        for idx, comp in values:
            indexes.append(idx)
            components.append(comp)

        return indexes, components

    @staticmethod
    def apply_threshold_approach(team_metrics, approach = ThresholdApproach.MTA):
        if approach == ThresholdApproach.minTA.value:
            return np.full(len(team_metrics), np.amin(team_metrics))
        else:
            return team_metrics

