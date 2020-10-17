from neat.enums.node_types import NodeType


class NodeGene:

    def __init__(self, node_type, depth, innovation_number=None):
        self.type = node_type
        self.depth = depth
        self.id = innovation_number

    def can_have_loop(self):
        """Check if suitable for loop link. """
        return (
            self.type != NodeType.BIAS and
            self.type != NodeType.INPUT
        )

    def valid_out(self):
        """Check if node can be used as out in link. """
        return (
            self.type != NodeType.BIAS and
            self.type != NodeType.INPUT
        )

    def is_output(self):
        return self.type == NodeType.OUTPUT

    def copy(self):
        return NodeGene(self.type, self.depth, self.id)
