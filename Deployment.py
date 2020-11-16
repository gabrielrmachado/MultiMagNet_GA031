from Reading import Parameterizer, FileType
from Preprocessing import Image, PreprocessingManager, Resize, Rotation, Smoothing
from MetricComputation import Metric, MetricComputation, ThresholdApproach
from Components import Factory, Component
from Detection import Detection
from Reformation import Reformation

class ExecutionManager:
    def __init__(self, folder_fbest_tb_files = "/data/files"):
        parameterizer = Parameterizer(FileType.Fbest_file)

        # reads the best set of parameters 'Fb' and its corresponding thresholds set 'Tb' obtained by the Calibration Stage.
        self.__fb = parameterizer.get_parameters()
        self.__tb = parameterizer.get_parameters(True)

