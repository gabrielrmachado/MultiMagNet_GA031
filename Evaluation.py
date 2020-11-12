from Helper import Helper
from MetricComputation import MetricComputation, Metric, ThresholdApproach
import numpy as np
import json
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
        votes = np.zeros(shape=(len(self.__combinations), len(self.__data)), dtype=int)
        team_metrics = np.zeros(len(members))

        for i in range(len(self.__combinations)):

            for j in range(len(self.__data)):
                
                votes_members = np.zeros(len(members), dtype=int)

                for k in range(len(members)):
                    rec_image = members[k].execute(self.__data[j])
                    team_metrics[k] = m.get_metric(self.__combinations[i][1]).compute(self.__data[j], rec_image, self.__true_labels[j])
                
                ta_metrics = Helper.apply_threshold_approach(team_metrics, self.__combinations[i][2])

                for k in range(len(ta_metrics)):
                    metric = ta_metrics[k]

                    if metric <= self.__tau_set[i][idx[k]]:
                        votes_members[k] = 0 # image classified as legitimate by member 'j' of the ensemble.
                    else: 
                        votes_members[k] = 1 # image classified as adversarial by member 'j' of the ensemble. 

                ensemble_vote = np.bincount(votes_members).argmax()
                votes[i][j] = ensemble_vote

            self.__accuracies[i] = accuracy_score(self.__true_labels, votes[i])

        # get the combination which has produced the largest accuracy.
        best_combination_idx = self.__accuracies.argmax()
        self.__best_combination["fp"] = self.__combinations[best_combination_idx][0]
        self.__best_combination["m"] = self.__combinations[best_combination_idx][1].value
        self.__best_combination["a"] = self.__combinations[best_combination_idx][2].value

        with open("data/files/fbest.json", 'w') as fbest_file:
            json.dump(self.__best_combination, fbest_file)

# from Data import ImageDAO, Dataset, AttackAlgorithm
# from Components import Factory, Component

# f = Component()

# sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
#     f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

# m = MetricComputation([0.01, 0.02, 0.05, 0.1], [Metric.RE, Metric.JSD], [ThresholdApproach.MTA, ThresholdApproach.minTA], ImageDAO.get_images(100)[0], sset)

# tau_set, combinations = m.get_tau_set()
# vdata, vlabels = ImageDAO.get_Vdataset(200, AttackAlgorithm.FGSM, eps=0.3)
# a = Assessment(vdata, vlabels, tau_set, sset, combinations)
# a.evaluate(m)

