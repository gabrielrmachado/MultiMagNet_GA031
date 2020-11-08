from abc import ABC, abstractmethod
from enum import Enum 
import time
import random

class IComponent(ABC):
    def __init__(self, image, id):
        self._image = image
        self._id = id

    @abstractmethod
    def execute(self): raise NotImplementedError

class CAE(IComponent):
    def __init__(self, image, id):
        super().__init__(image, id)

    def execute(self):
        print("CAE {0} is reconstructing the image...".format(self._id))
        time.sleep(1.5)
        print("CAE finished.")
        return self._image, True
        

class DAE(IComponent):
    def __init__(self, image, id):
        super().__init__(image, id)

    def execute(self):
        print("DAE {0} is reconstructing the image...".format(self._id))
        time.sleep(1.5)
        print("DAE finished.")
        return self._image, True

class GAN(IComponent):
    def __init__(self, image, id):
        super().__init__(image, id)

    def execute(self):
        print("GAN {0} is reconstructing the image...".format(self._id))
        time.sleep(2)
        print("GAN finished.")
        return self._image, True

class ComponentFactory(ABC):
    @abstractmethod
    def __init__(self, image):
        self._id = random.randint(1, 10)
        self._image = image

    def create(self): raise NotImplementedError

class CAEFactory(ComponentFactory):
    def __init__(self, image):
        super().__init__(image)
        
    def create(self): 
        return CAE(self._image, self._id)


class DAEFactory(ComponentFactory):
    def __init__(self, image):
        super().__init__(image)

    def create(self): 
        return DAE(self._image, self._id)


class GANFactory(ComponentFactory):
    def __init__(self, image):
        super().__init__(image)

    def create(self): 
        return GAN(self._image, self._id)

class Factory(Enum):
    CAE = 1
    DAE = 2
    GAN = 3

class Component:
    def __init__(self):
        self.__component: ComponentFactory

    def getComponent(self, image, factory: Factory):
        if factory == Factory.CAE:
            self.__component = CAEFactory(image).create()

        elif factory == Factory.DAE:
            self.__component = DAEFactory(image).create()

        elif factory == Factory.GAN:
            self.__component = GANFactory(image).create()

        return self.__component

# component = Component()
# component.getComponent(None, Factory.CAE).execute()
# component.getComponent(None, Factory.GAN).execute()
