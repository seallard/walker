from neat.enums.node_types import NodeType
from math import exp


class Node:

    def __init__(self, node_gene):
        self.in_links = []
        self.out_links = []
        self.type = node_gene.type
        self.id = node_gene.id
        self.output = 0
        self.activation_count = 0


    def activate(self):
        signal = 0

        for link in self.in_links:
            signal += link.from_node.output * link.weight

        self.output = 1 / (1 + exp(-signal))
        self.activation_count += 1

    def is_output(self):
        return self.type == NodeType.OUTPUT
