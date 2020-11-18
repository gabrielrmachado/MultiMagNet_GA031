from abc import ABC, abstractmethod
from enum import Enum
import json

class FileType(Enum):
    F_file = 1
    Fbest_file = 2
    Tb_file = 3

class IFile(ABC):
    @abstractmethod
    def read(self, ffile_path) -> dict: raise NotImplementedError

class FFile(IFile):
    def write(self, path, **calibration_params):
        with open(path, 'w') as ffile_file:
            json.dump(calibration_params, ffile_file)
    def read(self, path):
        with open(path) as ffile_file:
            return json.load(ffile_file)

class FBestFile(IFile):
    def read(self, path):
        with open(path) as fbest_file:
            return json.load(fbest_file)

class TbFile(IFile):
    def read(self, path):
        with open(path) as tb_file:
            return json.load(tb_file)

class Parameterizer:
    def __init__(self, path = "data/files"):
        self.__file: IFile
        self.__path = path
    
    def get_parameters(self, fileType: FileType):
        import os

        if fileType == FileType.F_file:
            self.__file = FFile()
            path = os.path.join(self.__path, "ffile.json")
        elif fileType == FileType.Fbest_file:
            self.__file = FBestFile()
            path = os.path.join(self.__path, "fbest.json")
        else:
            self.__file = TbFile()
            path = os.path.join(self.__path, "tb.json")

        return self.__file.read(path)

