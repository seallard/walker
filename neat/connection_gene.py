
class ConnectionGene:

    def __init__(self, from_node, to_node, weight, enabled, recurrent, innovation_number):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.enabled = enabled
        self.recurrent = recurrent
        self.innovation_number = innovation_number
