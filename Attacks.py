from abc import ABC, abstractmethod
from enum import Enum 
import time

class AttackAlgorithm(Enum):
    NONE = 0
    FGSM = 1
    DeepFool = 2
    CW = 3
    BIM = 4

class Attack:
    def set_attack(self, images, algorithm: AttackAlgorithm, **atk_params):
        self.__params = atk_params
        self.__attack: IAttack
       
        if algorithm == AttackAlgorithm.FGSM:
            self.__attack = FGSM(images)
        elif algorithm == AttackAlgorithm.DeepFool:
            self.__attack = DeepFool(images)
        elif algorithm == AttackAlgorithm.BIM:
            self.__attack = BIM(images)
        elif algorithm == AttackAlgorithm.CW:
            self.__attack = CW(images)
    
    def perform_attack(self):
        return self.__attack.compute_perturbations(**self.__params)


class IAttack(ABC):
    def __init__(self, images):
        self._adv_images = images

    @abstractmethod
    def compute_perturbations(self, **atk_params): raise NotImplementedError

class FGSM(IAttack):
    def __init__(self, images):
        super().__init__(images)

    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for FGSM:")
        
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with FGSM...")
        time.sleep(1)
        print("FGSM done. {0} adversarial images crafted.\n".format(len(self._adv_images)))
        return self._adv_images

class BIM(IAttack):
    def __init__(self, images):
        super().__init__(images)

    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for BIM:")
        
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with BIM...")
        time.sleep(2)
        print("BIM done. {0} adversarial images crafted.\n".format(len(self._adv_images)))
        return self._adv_images

class DeepFool(IAttack):
    def __init__(self, images):
        super().__init__(images)

    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for DeepFool:")
        
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with DeepFool...")
        time.sleep(3)
        print("DeepFool done. {0} adversarial images crafted.\n".format(len(self._adv_images)))
        return self._adv_images

class CW(IAttack):
    def __init__(self, images):
        super().__init__(images)

    def compute_perturbations(self, **atk_params):
        print("Parameters chosen for CW:")
       
        for param in atk_params:
            print("{0}: {1}".format(param, atk_params[param]))

        print("Attacking images with CW...")
        time.sleep(4)
        print("CW done. {0} adversarial images crafted.\n".format(len(self._adv_images)))
        return self._adv_images