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
    r: the repository object;
    combinations: the list containing the parameter's combinations.
    """
    def __init__(self, Vdata, Vlabels, tau_set, r, combinations):
        self.__data = Vdata
        self.__true_labels = Vlabels
        self.__best_combination = {'fp': None, 'm': None, 'a': None}
        self.__tau_set = tau_set
        self.__r = r
        self.__sset = r.getSSet()
        self.__combinations = combinations
        self.__accuracies = np.zeros(len(self.__combinations))

    def evaluate(self, m: MetricComputation, save_parameters=True):
        # always forms up an ensemble containing an odd number of members.
        idx, members = self.__r.getEnsembleMembers(random.randrange(1, len(self.__sset), 2))
        votes = np.zeros(shape=(len(self.__combinations), len(self.__data)), dtype=int)
        team_metrics = np.zeros(len(members))

        for i in range(len(self.__combinations)):

            for j in range(len(self.__data)):
                
                votes_members = np.zeros(len(members), dtype=int)

                for k in range(len(members)):
                    rec_image = members[k].execute(self.__data[j])
                    team_metrics[k] = m.get_metric(self.__combinations[i][1]).compute(self.__data[j], rec_image, self.__true_labels[j])
                
                ta_metrics = MetricComputation.apply_threshold_approach(team_metrics, self.__combinations[i][2])

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
        self.__best_combination["m"] = self.__combinations[best_combination_idx][1]
        self.__best_combination["a"] = self.__combinations[best_combination_idx][2]
        
        # get the Tb thresholds set which produced the largest accuracy.
        indexes = [i for i in range(len(self.__sset))]
        self.__tb = dict(zip(indexes, self.__tau_set[best_combination_idx]))

        if save_parameters == True:
            # saves the best combination and their corresponding thresholds in the 'fbest.json' and 'thresholds.json' for future use.
            with open("data/files/fbest.json", 'w') as fbest_file:
                json.dump(self.__best_combination, fbest_file)

            with open("data/files/tb.json", 'w') as tb_file:
                json.dump(self.__tb, tb_file)
