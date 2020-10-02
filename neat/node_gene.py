from neat.enums.node_types import NodeType


class NodeGene:

    def __init__(self, node_type, depth, innovation_number=None, recurrent=False):
        self.node_type = node_type
        self.depth = depth
        self.id = innovation_number
        self.recurrent = recurrent

    def can_have_loop(self):
        """Check if suitable for loop link. """
        return (
            not self.recurrent and
            self.node_type != NodeType.BIAS and
            self.node_type != NodeType.INPUT
        )

    def valid_out(self):
        """Check if node can be used as out in link. """
        return (
            self.node_type != NodeType.BIAS and
            self.node_type != NodeType.INPUT
        )

    def is_output(self):
        return self.node_type == NodeType.OUTPUT

    def copy(self):
        return NodeGene(self.node_type, self.depth, self.id, self.recurrent)
