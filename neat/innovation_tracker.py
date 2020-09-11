
class InnovationTracker:

    def __init__(self):
        self.connection_innovations = {}
        self.node_innovations = {}
        self.connection_innovation_number = 0 # TODO: read from config, inputs*outputs
        self.node_innovation_number = 0 # TODO: read from config, inputs + outputs

    def get_innovation_number(self, in_node, out_node, innovation_type):
        """
        Returns innovation number for existing innovation or generates and
        saves a new one, if the innovation is new.
        """
        pass

    def reset(self):
        pass
