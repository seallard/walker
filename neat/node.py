from neat.enums.node_types import NodeType
import math


class Node:

    def __init__(self, node_gene):
        self.in_links = []
        self.out_links = []
        self.node_type = node_gene.node_type
        self.id = node_gene.id
        self.output = 0


    def activate(self):
        signal = 0

        for link in node.in_links:
            signal += link.from_node.output * link.weight
        
        return 1 / (1 + math.exp(-signal))

    def is_output(self):
        return self.node_type == NodeType.OUTPUT
