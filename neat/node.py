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
        self.active = False # Whether the node has any active inputs. Only relevant for start.
        self.sum = 0 # Keep track of net input signal.

    def activate(self):

        if self.active:
            self.activation_count += 1
            self.output = 1 / (1 + exp(-self.sum)) # Sigmoid activation.
            self.sum = 0 # Reset net input signal.

    def calculate_net_input_signal(self):
        for link in self.in_links:
            if link.from_node.active:
                self.sum += link.from_node.output * link.weight
                self.active = True # The node has active inputs and is therefor active.

    def is_output(self):
        return self.type == NodeType.OUTPUT
