from Helper import Helper
from Components import IComponent

class Reformation:
    def __init__(self, reformers, image):
        self.__reformer: IComponent
        self.__reformer = Helper.getEnsembleMembers(reformers, 1)
        self.__image = image

    def reformer(self):
        return self.__reformer.execute(self.__image)