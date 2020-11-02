

class InnovationTracker:
    """Keeps track of the innovations (hidden nodes and links).

    The innovations are stored in a dictionary. The innovations are specified by
    two nodes. The innovation occurs between them, as a new node or link.
    """

    def __init__(self, config):
        self.link_innovations = {}
        self.node_innovations = {}
        self.next_node_id = config.num_inputs + config.num_outputs + 1 # One bias node.
        self.next_link_id = 0

    def assign_node_id(self, first_node_id, second_node_id, gene):

        key = (first_node_id, second_node_id, type(gene))

        try:
            gene.id = self.node_innovations[key]

        except:
            gene.id = self.next_node_id
            self.node_innovations[key] = self.next_node_id
            self.next_node_id += 1

    def assign_link_id(self, gene):
        key = (gene.from_node.id, gene.to_node.id, type(gene))

        try:
            gene.id = self.link_innovations[key]

        except:
            gene.id = self.next_link_id
            self.link_innovations[key] = self.next_link_id
            self.next_link_id += 1
