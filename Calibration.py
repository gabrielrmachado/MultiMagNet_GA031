from Authentication import User
from Reading import FileType, Parameterizer
from Data import ImageDAO, Dataset, AttackAlgorithm
from Components import Factory, Component
from MetricComputation import Metric, MetricComputation, ThresholdApproach
from Evaluation import Assessment

class ParameterTuning:
    def __init__(self):
        user = User()

        # simulates the login operation of an user.
        userID = input("Welcome to the Calibration Stage of MultiMagNet! Type your user ID: ")
        user.login(userID)
        
        if user.get_priority_logged_user() > 1:
            raise PermissionError("Sorry, user {0} is not allowed to perform calibrations on MultiMagNet.".format(user.get_name_user()))

    def calibrate(self, qty_vleg_images):
        # simulates the loading process of all the components from S set.
        f = Component()
        
        sset = [f.getComponent(Factory.CAE), f.getComponent(Factory.DAE), f.getComponent(Factory.GAN), f.getComponent(Factory.CAE), 
            f.getComponent(Factory.DAE), f.getComponent(Factory.GAN)]

        # reads parameters from F file to be tested.
        file_reader = Parameterizer(FileType.F_file)
        params = file_reader.get_parameters()
        m = MetricComputation(params['fp'], params['m'], params['a'], ImageDAO.get_images(qty_vleg_images)[0], sset)

        # computes 'Tau' set and saves the best set of parameters in 'fbest.json' file.
        tau_set, combinations = m.get_tau_set()
        vdata, vlabels = ImageDAO.get_Vdataset(qty_vleg_images*2, AttackAlgorithm.FGSM, eps=0.3)
        a = Assessment(vdata, vlabels, tau_set, sset, combinations)
        a.evaluate(m)

p = ParameterTuning()
p.calibrate(150)