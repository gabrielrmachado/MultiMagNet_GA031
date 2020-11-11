from Helper import Helper
from MetricComputation import MetricComputation, Metric, ThresholdApproach
import numpy as np
import random
from sklearn.metrics import accuracy_score

class Assessment:
    """
    Evaluates the thresholds computed from legitimate images in the V dataset.

    Parameters:
    -----------
    Vdata: the V dataset containing both legitimate and adversarial images;
    Vlabels: the corresponding labels for each image in the V dataset;
    tau_set: the set containing the 'm.c' thresholds (computed from legitimate images)
    s_set: the set containing 'm' defense components, used to compute the Tau_set;
    combinations: the list containing the parameter combinations.
    """
    def __init__(self, Vdata, Vlabels, tau_set, s_set, combinations):
        self.__data = Vdata
        self.__true_labels = Vlabels
        self.__best_combination = {'fp': None, 'm': None, 'a': None}
        self.__tau_set = tau_set
        self.__s_set = s_set
        self.__combinations = combinations
        self.__accuracies = np.zeros(len(self.__combinations))


    def evaluate(self, m: MetricComputation):
        # always forms up an ensemble containing an odd number of members.
        idx, members = Helper.getEnsembleMembers(self.__s_set, numMembers=random.randrange(1,len(self.__s_set),2))
        votes = np.zeros(shape=(len(self.__combinations), len(members), len(self.__data)))

        for i in range(len(self.__combinations)):

            for j in range(len(members)):

                for k in range(len(self.__data)):
                        rec_image = members[j].execute(self.__data[k])
                        metric = m.get_metric(self.__combinations[i][1]).compute(self.__data[k], rec_image)

                        if metric <= self.__tau_set[idx[j]]:
                            votes[i][j][k] = 0 # image classified as legitimate by member 'j' of the ensemble.
                        else: 
                            votes[i][j][k] = 1 # image classified as adversarial by member 'j' of the ensemble.
            
            self.__accuracies[i] = accuracy_score(self.__true_labels, votes[i][j].flatten())

        print(self.__accuracies, self.__accuracies.shape)
            
class Filewriter:
    def __init__(self, fbest_file_path="data/fbest.json", **best_parameters):
        pass

from Data import ImageDAO, Dataset, AttackAlgorithm
from Components import Factory, Component

f = Component()

sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
    f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

m = MetricComputation([0.1, 0.2, 0.3, 0.25], [Metric.RE, Metric.JSD], [ThresholdApproach.MTA], ImageDAO.get_images(100)[0], sset)

tau_set, combinations = m.get_tau_set()

vdata, vlabels = ImageDAO.get_Vdataset(200, AttackAlgorithm.FGSM, eps=0.3)
a = Assessment(vdata, vlabels, tau_set, sset, combinations)
a.evaluate(m)

