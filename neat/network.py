import networkx as nx
import matplotlib.pyplot as plt
from neat.enums.node_types import NodeType


class Network:

    def __init__(self, nodes, links, num_inputs, num_outputs):
        self.nodes = nodes
        self.links = links
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

    def activate(self, inputs, stabilize):
        """Propagate input through network until each output is activated.
           Precondition: nodes are ordered as [bias, inputs, outputs, hidden]
        """

        # Initialise bias node.
        self.nodes[0].output = 1
        self.nodes[0].active = True

        # Initialise input nodes with inputs.
        for i, node in enumerate(self.nodes[1:self.num_inputs + 1]):
            node.output = inputs[i]
            node.active = True

        if stabilize:
            max_tries = len(self.links) + 5

        else:
            max_tries = 1

        tries = 0

        while tries < max_tries: # Dirty way: cleaner to check if outputs are stable.

            # Iterate over nodes and calculate their net input signals.
            for node in self.nodes[self.num_inputs + 1:]:
                node.calculate_net_input_signal()

            # Activate each node based on their net input signal.
            for node in self.nodes[self.num_inputs + 1:]:
                node.activate()

            tries += 1

        return self.get_outputs()

    def draw(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(self.nodes)

        color_map = []
        node_labels = {}

        for node in self.nodes:
            if node.type == NodeType.INPUT:
                color_map.append('green')

            elif node.type == NodeType.HIDDEN:
                color_map.append('blue')

            elif node.type == NodeType.BIAS:
                color_map.append('yellow')

            else:
                color_map.append("red")

            node_labels[node] = node.id

        edge_labels = {}

        for link in self.links:
            graph.add_edge(link.from_node, link.to_node)
            edge_labels[(link.from_node, link.to_node)] = link.id

        positioning = nx.spring_layout(graph)
        nx.draw(graph, pos=positioning, labels=node_labels, edge_color='black', arrowsize=10, node_color=color_map, alpha=0.5)
        nx.draw_networkx_edge_labels(graph, positioning, edge_labels=edge_labels)
        plt.show()

    def get_outputs(self):
        output_nodes = self.nodes[self.num_inputs + 1:self.num_inputs+self.num_outputs + 1]
        return [node.output for node in output_nodes]

    def reset(self):
        """Remove any signals in the network. """

        for node in self.nodes:
            node.reset()
