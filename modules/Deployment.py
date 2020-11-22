from Reading import Parameterizer, FileType
from Preprocessing import Image, PreprocessingManager, Resize, Rotation, Smoothing
from MetricComputation import Metric, MetricComputation, ThresholdApproach
from Components import Factory, Component
from Detection import Detection
from Reformation import Reformation
from Helper import Helper

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
        import random

        # preprocesses the image according to the settings in 'preprocessing_params'.
        preprocessing = PreprocessingManager(image, **preprocessing_params)
        preprocessing.apply()   

        indexes, _ = Helper.getEnsembleMembers(self.__sset, random.randrange(1, len(self.__sset), 2))    
        vm = []
        tb_members = []

        # gets the metric values of each member for the input image.
        for i in indexes:
            rec_image = self.__sset[i].execute(image.get_image_arr())
            is_adv = random.randint(0, 1)

            value_metric = MetricComputation.get_metric(Metric(self.__fb["m"])).compute(image.get_image_arr(), rec_image, is_adv)
            vm.append(value_metric)
        
        for i in [str(idx) for idx in indexes]:
            tb_members.append(self.__tb[i])

        # apply the threshold approach.
        tb_members = Helper.apply_threshold_approach(tb_members, self.__fb['a'])

        # checks whether the input image is adversarial or not.
        d = Detection(vm, tb_members)
        ans = d.detect()

        print("\nImage {0} is {1}".format(image.get_image_id(), "legitimate" if is_adv == 0  else "adversarial"))

        if ans == False:
            print("Image {0} has been detected as adversarial and will be discarded.\n".format(image.get_image_id()))
        else:
            print("Image {0} is going to be reformed.\n".format(image.get_image_id()))
            # if the image is considered as legitimate, it is reformed.
            r = Reformation(self.__sset, image)
            r.reform()

        
