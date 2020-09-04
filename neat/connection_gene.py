import random

class ConnectionGene:

    def __init__(self, in_node, out_node, enabled=True, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = self.__assign_random_weight()
        self.enabled = enabled
        self.innovation_number = innovation_number

    def __assign_random_weight():
        return random.random()
