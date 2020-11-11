import random

class Helper:
    @staticmethod
    def getEnsembleMembers(S_set, numMembers: int):
        if numMembers % 2 != 0:
            raise ArithmeticError("Number of members must be odd.")
        return random.sample(S_set, numMembers)


