from abc import ABC, abstractmethod
from enum import Enum 
import time
import random

class IComponent(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def execute(self, image): raise NotImplementedError

class CAE(IComponent):
    def __init__(self, id):
        super().__init__(id)

    def execute(self, image):
        # print("CAE {0} is reconstructing the image...".format(self._id))
        image_ref = image.copy()
        # print("CAE finished.")
        return image_ref        

class DAE(IComponent):
    def __init__(self, id):
        super().__init__(id)

    def execute(self, image):
        # print("DAE {0} is reconstructing the image...".format(self._id))
        image_ref = image.copy()
        # print("DAE finished.")
        return image_ref

class GAN(IComponent):
    def __init__(self, id):
        super().__init__(id)

    def execute(self, image):
        # print("GAN {0} is reconstructing the image...".format(self._id))
        image_ref = image.copy()
        # print("CAE finished.")
        return image_ref

class ComponentFactory(ABC):
    @abstractmethod
    def __init__(self):
        self._id = random.randint(1, 10)

    def create(self): raise NotImplementedError

class CAEFactory(ComponentFactory):
    def __init__(self):
        super().__init__()
        
    def create(self): 
        return CAE(self._id)


class DAEFactory(ComponentFactory):
    def __init__(self):
        super().__init__()

    def create(self): 
        return DAE(self._id)


class GANFactory(ComponentFactory):
    def __init__(self,):
        super().__init__()

    def create(self): 
        return GAN(self._id)

class Factory(Enum):
    CAE = 1
    DAE = 2
    GAN = 3

class Repository:
    def __init__(self):
        self.__component: ComponentFactory
        self._sset = []

    def __getComponent(self, factory: Factory):
        if factory == Factory.CAE:
            self.__component = CAEFactory().create()

        elif factory == Factory.DAE:
            self.__component = DAEFactory().create()

        elif factory == Factory.GAN:
            self.__component = GANFactory().create()

        return self.__component

    def getSSet(self):
        self._sset = [self.__getComponent(Factory.CAE), self.__getComponent(Factory.DAE), self.__getComponent(Factory.GAN), self.__getComponent(Factory.CAE), 
            self.__getComponent(Factory.DAE), self.__getComponent(Factory.GAN)]
        
        return self._sset

    def getEnsembleMembers(self, numMembers: int):
        """
        Receives the S set and choose randomly an odd number of members.

        Returns:
        --------------

        indexes (list): a list with the corresponding chosen indexes in S set;
        components (list): a list containing the corresponding components, represented by the 'indexes' list.
        """

        if numMembers < 1 or numMembers > len(self._sset):
            raise AttributeError("Invalid number.")
        elif numMembers % 2 == 0:
            raise ArithmeticError("Number of members must be odd.")
       

        values = random.sample(list(enumerate(self._sset)), numMembers)        
        indexes = []
        components = []
        
        for idx, comp in values:
            indexes.append(idx)
            components.append(comp)

        return indexes, components

    

    
