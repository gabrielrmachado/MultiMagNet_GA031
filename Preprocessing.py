from abc import ABC, abstractmethod
from enum import Enum 
from mnist import MNIST
import time, math

class IPreprocessor(ABC):
    @abstractmethod
    def apply(self): raise NotImplementedError

class Image(IPreprocessor):
    def __init__(self, image, imageID):
        self.__mnist_data = MNIST()
        self._image = image
        self.__id = imageID
        
    def print_image(self):
        print(self.__mnist_data.display(self._image))

    def get_shape(self):
        h = math.sqrt(len(self._image))
        print("{0}x{1}x{2}".format(h, h, 1))

    def apply(self):
        return "Image {0}".format(self.__id)

class PreprocessorDecorator(IPreprocessor, ABC):
    def __init__(self, image: IPreprocessor, *params):
        self._image = image
        self._params = params

    def apply(self):
        return self._image.apply()

class Rotation(PreprocessorDecorator):
    def __init__(self, image: IPreprocessor, *params):
        super().__init__(image, *params)

    def apply(self):
        return self._image.apply() + ", rotated {0} degrees".format(self._params[0])

class Resize(PreprocessorDecorator):
    def __init__(self, image: IPreprocessor, *params):
        super().__init__(image, *params)

    def apply(self):
        return self._image.apply() + ", resized to {0}x{1}x1".format(self._params[0], self._params[1])

class Smoothing(PreprocessorDecorator):
    def __init__(self, image: IPreprocessor, *params):
        super().__init__(image, *params)

    def apply(self):
        return self._image.apply() + ", smoothed"

image = Image(None, 23)
image_prepr = Resize(Smoothing(Rotation(image, 90), []), 32,16)
print(image_prepr.apply())