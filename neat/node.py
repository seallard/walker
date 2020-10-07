from neat.enums.node_types import NodeType
from math import exp


class Node:

    def __init__(self, node_gene):
        self.in_links = []
        self.out_links = []
        self.type = node_gene.type
        self.id = node_gene.id
        self.output = 0


    def activate(self):
        signal = 0

        for link in node.in_links:
            signal += link.from_node.output * link.weight

        return 1 / (1 + exp(-signal))

    def is_output(self):
        return self.type == NodeType.OUTPUT
