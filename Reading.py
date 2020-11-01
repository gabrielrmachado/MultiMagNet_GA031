from abc import ABC, abstractmethod

class IFile(ABC):
    @abstractmethod
    def read(self): raise NotImplementedError

class FFile(IFile):
    def read(self):
        print("FFile file")

class FBestFile(IFile):
    def read(self):
        print("FBestFile file")

class File:
    pass

class Parameterizer:
    def __init__(self, file):
        if isinstance(file, IFile) == False:
            raise TypeError("file object does not implement IFile interface.")
        self.__file = file
    
    def getParameters(self):
        self.__file.read()


p = Parameterizer(FBestFile())
p.getParameters()
