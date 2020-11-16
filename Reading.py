from abc import ABC, abstractmethod
from enum import Enum
import json

class FileType(Enum):
    F_file = 1
    Fbest_file = 2

class IFile(ABC):
    @abstractmethod
    def read(self, ffile_path) -> dict: raise NotImplementedError

class FFile(IFile):
    def write(self, ffile_path, **calibration_params):
        with open(ffile_path, 'w') as ffile_file:
            json.dump(calibration_params, ffile_file)
    def read(self, ffile_path):
        with open(ffile_path) as ffile_file:
            return json.load(ffile_file)

class FBestFile(IFile):
    def read(self, ffile_path):
        with open(ffile_path) as fbest_file:
            return json.load(fbest_file)

class Parameterizer:
    def __init__(self, fileType: FileType, path = "data/files"):
        import os
        self.__file: IFile

        if fileType == FileType.F_file:
            self.__file = FFile()
            self.__path = path = os.path.join(path, "ffile.json")
        else:
            self.__file = FBestFile()
            self.__path = path = os.path.join(path, "fbest.json")

    # def write_ffile(self, **params):
    #     self.__file.__class__ = FFile
    #     self.__file.write(self.__path, **params)
    
    def get_parameters(self):
        return self.__file.read(self.__path)

# from MetricComputation import Metric, MetricComputation, ThresholdApproach
# p = Parameterizer(FileType.F_file)
# # p.write_ffile(fp=[0.01, 0.02, 0.05, 0.1], m=[Metric.RE.value, Metric.JSD.value], a=[ThresholdApproach.MTA.value, ThresholdApproach.minTA.value])
# params = p.get_parameters()
# print(params["fp"])
