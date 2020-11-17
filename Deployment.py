from Reading import Parameterizer, FileType
from Preprocessing import Image, PreprocessingManager, Resize, Rotation, Smoothing
from MetricComputation import Metric, MetricComputation, ThresholdApproach
from Components import Factory, Component
from Detection import Detection
from Reformation import Reformation

class ExecutionManager:
    def __init__(self, folder_fbest_tb_files = "/data/files"):
        parameterizer = Parameterizer()

        # reads the best set of parameters 'Fb' and its corresponding thresholds set 'Tb' obtained by the Calibration Stage.
        self.__fb = parameterizer.get_parameters(FileType.Fbest_file)
        self.__tb = parameterizer.get_parameters(FileType.Tb_file)

        # loads the S set.
        f = Component()
        self.__sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
            f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]


    def run(self, image: Image, **preprocessing_params):
        # preprocesses the image according to the settings in 'preprocessing_params'.
        preprocessing = PreprocessingManager(image, **preprocessing_params)
        preprocessing.apply()

        # computes the Vm set.
        m = MetricComputation(self.__fb["fp"], self.__fb["m"], self.__fb["a"], image, self.__sset, False)
        vm = m.get_tau_set()

        # checks whether the input image is adversarial or not.
        d = Detection(vm, self.__tb)
        ans = d.detect()

        if ans == False:
            print("Image {0} has been detected as adversarial and will be discarted.")
        else:
            # if the image is considered as legitimate, it is reformed.
            r = Reformation(self.__sset, image)
            r.reformer()

e = ExecutionManager()

from Data import ImageDAO
e.run(Image(ImageDAO.get_images(1), 25), ro=90, rz="32x32", sm=[])

        
