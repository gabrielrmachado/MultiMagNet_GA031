from Helper import Helper
import numpy as np
import random

class Assessment:
    """
    Evaluates the thresholds computed from legitimate images in the V dataset.

    Parameters:
    -----------
    Vdata: the V dataset containing both legitimate and adversarial images;
    Vlabels: the corresponding labels for each image in the V dataset;
    Tau_set: the set containing the 'm.c' thresholds (computed from legitimate images)
    S_Set: the set containing 'm' defense components, used to compute the Tau_set;

    """
    def __init__(self, Vdata, Vlabels, Tau_set, S_set):
        self.__data = Vdata
        self.__true_labels = Vlabels
        self.__best_combination = {'fp': None, 'm': None, 'a': None}
        self.__tau_set = Tau_set
        self.__s_set = S_set

        c = len(Tau_set) / len(S_set)
        self.__accuracies = np.zeros(shape=(len(S_set), c))                

    def evaluate(self, fa):
        # always forms up an ensemble containing an odd number of members.
        members = Helper.getEnsembleMembers(self.__s_set, numMembers=random.randrange(1,10,2))
        self.__metrics = np.zeros(shape=(len( self.__data), len(members)))
        
        for i in len(self.__data):
            for j in len(members):
                pass

class Filewriter:
    def __init__(self, fbest_file_path="data/fbest.json", **best_parameters):
        pass


