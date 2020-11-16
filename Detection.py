from Helper import Helper
import numpy as np

class Detection:
    def __init__(self, Vm, Tb):
        self.__vm = Vm
        self.__tb = Tb

    def detect(self):
        qleg = 0
        qadv = 0

        for i in range(len(self.__vm)):
            if self.__vm[i] <= self.__tb[i]: 
                qleg = qleg + 1 # voted as legitimate by member 'i' of the ensemble
            else:
                qadv = qadv + 1 # otherwise

        if qleg > qadv: return True
        else: return False