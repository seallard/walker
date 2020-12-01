from random import uniform
from neat.enums.node_types import NodeType


class LinkGene:
    __slots__ = ['from_node', 'to_node', 'enabled', 'recurrent', 'weight', 'id']
    def __init__(self, from_node, to_node, enabled=True, recurrent=False):
        self.from_node = from_node
        self.to_node = to_node
        self.enabled = enabled
        self.recurrent = recurrent
        self.id = id
        self.weight = uniform(-1, 1)

    def can_be_split(self):
        return (
            self.enabled and
            not self.recurrent and
            self.from_node.type != NodeType.BIAS
        )

    def copy(self, from_node, to_node):
        copy = LinkGene(from_node, to_node, self.enabled, self.recurrent)
        copy.id = self.id
        copy.weight = self.weight
        return copy
