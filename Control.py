from Calibration import ParameterTuning
from Deployment import ExecutionManager
from Data import ImageDAO # simulation purposes only.
from Preprocessing import Image # simulation purposes only.
from random import randint
from time import sleep
import os

class MultiMagNet:       

    def run(self):
        print("Welcome to MultiMagNet!\n\nWhat do you want to do?\n1- Calibrate MultiMagNet;\n2- Detect input images.")
        op = int(input("\nYour answer: "))
        
        while op > 2 or op < 1:
            op = int(input("Invalid answer. Please choose a valid option: "))

        os.system("clear")
        
        if op == 1:
            self.__calibrator = ParameterTuning()
            qtd = input("How many legitimate images from VLeg do you want to use in order to calibrate MultiMagNet? ")
            self.__calibrator.calibrate(int(qtd))
        else:
            print("Running MultiMagNet...\n")
            self.__runner = ExecutionManager()
            qtd_dummy_images = 100
            images = []
            dummy_images, _ = ImageDAO.get_images(qtd_dummy_images)

            # creating dummy image objects in order to simulate the capture system...
            for i in range(qtd_dummy_images):
                images.append(Image([dummy_images[i]], randint(1, qtd_dummy_images)))

            for i in range(qtd_dummy_images):
                print("Analysing image {0}...".format(images[i].get_image_id()))
                sleep(0.1)
                self.__runner.run(images[i], ro=90, rz=[32,32], sm=[])
        
multimagnet = MultiMagNet()
multimagnet.run()