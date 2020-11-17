from Helper import Helper
from Components import IComponent

class Reformation:
    def __init__(self, reformers, image):
        self.__reformer: IComponent
        _, self.__reformer = Helper.getEnsembleMembers(reformers, 1)
        self.__image = image

    def reform(self):
        return self.__reformer[0].execute(self.__image.get_image_arr())