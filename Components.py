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
        print("CAE {0} is reconstructing the image...".format(self._id))
        image_ref = image.copy()
        print("CAE finished.")
        return image_ref        

class DAE(IComponent):
    def __init__(self, id):
        super().__init__(id)

    def execute(self, image):
        print("DAE {0} is reconstructing the image...".format(self._id))
        image_ref = image.copy()
        print("DAE finished.")
        return image_ref

class GAN(IComponent):
    def __init__(self, id):
        super().__init__(id)

    def execute(self, image):
        print("GAN {0} is reconstructing the image...".format(self._id))
        image_ref = image.copy()
        print("CAE finished.")
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

class Component:
    def __init__(self):
        self.__component: ComponentFactory

    def getComponent(self, factory: Factory):
        if factory == Factory.CAE:
            self.__component = CAEFactory().create()

        elif factory == Factory.DAE:
            self.__component = DAEFactory().create()

        elif factory == Factory.GAN:
            self.__component = GANFactory().create()

        return self.__component

# component = Component()
# component.getComponent(None, Factory.CAE).execute()
# component.getComponent(None, Factory.GAN).execute()
