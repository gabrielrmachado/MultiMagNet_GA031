from Authentication import User
from Reading import FileType, Parameterizer
from Data import ImageDAO, Dataset, AttackAlgorithm
from Components import Factory, Component
from MetricComputation import Metric, MetricComputation, ThresholdApproach
from Evaluation import Assessment

class ParameterTuning:
    def __init__(self, userID=None, password=None):
        self.__userID = userID
        self.loggedUser = None
        user = User()
        
        # simulates the login operation of an user.
        if self.__userID is None:
            self.__userID = input("Welcome to the Calibration Stage of MultiMagNet! Type your user ID: ")
        
        user.login(self.__userID, password)
        
        if user.get_priority_logged_user() > 1:
            raise PermissionError("Sorry, user {0} is not allowed to perform calibrations on MultiMagNet.".format(user.get_name_user()))

        else: self.loggedUser = user                

    def calibrate(self, qtd_leg_images, save_parameters=True):
        # simulates the loading process of all the components from S set.
        f = Component()
        
        sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
            f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

        # reads parameters from F file to be tested.
        file_reader = Parameterizer()
        params = file_reader.get_parameters(FileType.F_file)
        m = MetricComputation(params['fp'], params['m'], params['a'], ImageDAO.get_images(qtd_leg_images)[0], sset)

        # computes 'Tau' set and saves the best set of parameters in 'fbest.json' file.
        tau_set, combinations = m.get_tau_set()
        vdata, vlabels = ImageDAO.get_Vdataset(qtd_leg_images, AttackAlgorithm.FGSM, eps=0.3)
        a = Assessment(vdata, vlabels, tau_set, sset, combinations)
        a.evaluate(m, save_parameters)

        print("\nFbest and Tb files have been saved successfully.")
        return True