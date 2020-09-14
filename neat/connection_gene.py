from random import random

class ConnectionGene:

    def __init__(self, from_node, to_node, enabled, recurrent):
        self.from_node = from_node
        self.to_node = to_node
        self.enabled = enabled
        self.recurrent = recurrent
        self.innovation_number = None
        self.weight = self.__randomise_weight()



    def __randomise_weight(self):
        """Sets weight to number between 0 and 1. """
        self.weight = random()
