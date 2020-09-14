from neat.enums.node_types import NodeType

class NodeGene:

    def __init__(self, node_type, node_id, recurrent=False):
        self.node_type = node_type
        self.id = node_id
        self.recurrent = recurrent


    def can_have_loop(self):
        """Check if suitable for loop connection. """
        return (
            not self.recurrent and
            self.node_type != NodeType.BIAS and
            self.node_type != NodeType.INPUT
        )

    def can_be_out_node(self):
        """Check if node can be used as out in link. """
        return (
            self.node_type != NodeType.BIAS and
            self.node_type != NodeType.INPUT
        )