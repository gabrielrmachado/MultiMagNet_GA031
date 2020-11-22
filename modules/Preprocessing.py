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
    
    def get_image_arr(self):
        return self._image[0]

    def get_image_id(self):
        return self.__id

    def get_shape(self):
        h = int(math.sqrt(len(self._image.get_image_arr())))
        return (h,h)

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
        from copy import deepcopy

        image = deepcopy(self._image)
        image.__class__ = Image
        
        if image.get_shape() != self._params:
            return self._image.apply() + ", resized to {0}x{1}x1".format(self._params[0], self._params[1])
        else:
            return self._image.apply() + ", no resized"

class Smoothing(PreprocessorDecorator):
    def __init__(self, image: IPreprocessor, *params):
        super().__init__(image, *params)

    def apply(self):
        return self._image.apply() + ", smoothed"


class PreprocessingManager:
    """
        Performs the preprocessing operations on the provided image.

        image (Image): the image object that will be preprocessed.
        **operations (dict):  the list of preprocessing techniques which will be applied in the image. They can be:
            - ro (rotation): simulates an image rotation. The degrees must be passed along (eg.: ro=30)
            - rz (resize): simulates an image resizing. The values must be passed along (eg.: rz="32x32")  
            - sm (smoothing): simulates an image smoothing. No values are passed. 
    """
    def __init__(self, image: Image, **operations):
        self.__message = ""
        self.__image = image
        self.__operations = operations

    def apply(self):
        for key in self.__operations.keys():
            if key == 'ro':
                self.__image = Rotation(self.__image, self.__operations[key])
            elif key == 'rz':
                self.__image = Resize(self.__image, self.__operations[key][0], self.__operations[key][1])
            elif key == 'sm':
                self.__image = Smoothing(self.__image, self.__operations[key])
        
        print(self.__image.apply())

        
