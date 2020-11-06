from abc import ABC, abstractmethod
from enum import Enum 
import time

class AttackAlgorithm(Enum):
    FGSM = 1
    DeepFool = 2
    CW = 3

class Attack:
    def set_attack(self, images, algorithm: AttackAlgorithm, **atk_params):
        self.__perturbedImages = images
        self.__params = atk_params
        self.__attack: IAttack
       
        if algorithm == AttackAlgorithm.FGSM:
            self.__attack = FGSM()
        elif algorithm == AttackAlgorithm.DeepFool:
            self.__attack = DeepFool()
        elif algorithm == AttackAlgorithm.CW:
            self.__attack = CW()
    
    def perform_attack(self):
        self.__attack.compute_perturbations(**self.__params)


class IAttack(ABC):
    @abstractmethod
    def compute_perturbations(self, **atk_params): raise NotImplementedError

class FGSM(IAttack):
    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for FGSM:")
        
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with FGSM attack...")
        time.sleep(1)
        print("FGSM done.\n")

class DeepFool(IAttack):
    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for DeepFool:")
        
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with DeepFool attack...")
        time.sleep(3)
        print("DeepFool done.\n")

class CW(IAttack):
    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for CW:")
       
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with CW attack...")
        time.sleep(4)
        print("CW done.\n")

attack = Attack()
attack.set_attack(None, AttackAlgorithm.FGSM, eps = 0.3, norm = "l2")
attack.perform_attack()
attack.set_attack(None, AttackAlgorithm.DeepFool, eps=0.03, n_iter=20, norm = "l2")
attack.perform_attack()