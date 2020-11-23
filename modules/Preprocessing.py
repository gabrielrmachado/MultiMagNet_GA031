from abc import ABC, abstractmethod
from enum import Enum 
from mnist import MNIST
from copy import deepcopy
import time, math

class IPreprocessor(ABC):
    @abstractmethod
    def apply(self): raise NotImplementedError

class Image(IPreprocessor):
    def __init__(self, image, imageID):
        self.__mnist_data = MNIST()
        self._image = image
        self.__id = imageID
        self._description = "Image {0}".format(self.__id)
        
    def print_image(self):
        print(self.__mnist_data.display(self._image))
    
    def get_image_arr(self):
        return self._image[0]

    def get_image_id(self):
        return self.__id

    def get_shape(self):
        h = int(math.sqrt(len(self.get_image_arr())))
        return (h,h)

    def apply(self):
        return self._description

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
        self._image._description = self._image.apply() + ", rotated {0} degrees".format(self._params[0])
        return self._image._description

class Resize(PreprocessorDecorator):
    def __init__(self, image: IPreprocessor, *params):
        super().__init__(image, *params)

    def apply(self):
        image = deepcopy(self._image)
        image.__class__ = Image
        
        if image.get_shape() != self._params:
            self._image._description = self._image.apply() + ", resized to {0}x{1}x1".format(self._params[0], self._params[1])
        else:
            self._image._description = self._image.apply() + ", no resized"
        
        return self._image._description 

class Smoothing(PreprocessorDecorator):
    def __init__(self, image: IPreprocessor, *params):
        super().__init__(image, *params)

    def apply(self):
        self._image._description = self._image.apply() + ", smoothed"
        return self._image._description


class PreprocessingManager:
    def __init__(self):
        self.__message = ""

    def apply(self, image: Image, **operations):
        """
        Performs the preprocessing operations on the provided image.

        image (Image): the image object that will be preprocessed.
        **operations (dict):  the list of preprocessing techniques which will be applied in the image. They can be:
            - ro (rotation): simulates an image rotation. The degrees must be passed along (eg.: ro=30)
            - rz (resize): simulates an image resizing. The values must be passed along (eg.: rz="32x32")  
            - sm (smoothing): simulates an image smoothing. No values are passed. 
        """
        for key in operations.keys():
            if key == 'ro':
                image = Rotation(image, operations[key])
            elif key == 'rz':
                image = Resize(image, operations[key][0], operations[key][1])
            elif key == 'sm':
                image = Smoothing(image, operations[key])
        
        self.__message = image.apply()
        print(self.__message)
        return self.__message

        
