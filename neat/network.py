import networkx as nx
import matplotlib.pyplot as plt
from neat.enums.node_types import NodeType


class Network:

    def __init__(self, nodes, links, num_inputs, num_outputs):
        self.nodes = nodes
        self.links = links
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.running = False

    def update(self, inputs):
        """Propagate input through network until each output is activated. """

        # Initialise input nodes with inputs.
        for i, node in enumerate(self.nodes[:self.num_inputs]):
            node.output = inputs[i]
            node.active = True

        #TODO: initialise bias node with 1.
        activated_once = False

        while self.output_inactive() or not activated_once:

            # Iterate over nodes and calculate their net input signals.
            for node in self.nodes[self.num_inputs:]:
                node.calculate_net_input_signal()

            # Activate each node based on their net input signal.
            for node in self.nodes[self.num_inputs:]:
                node.activate()

            activated_once = True

        return self.get_outputs()

    def draw(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(self.nodes)

        color_map = []
        for node in self.nodes:
            if node.type == NodeType.INPUT:
                color_map.append('green')

            elif node.type == NodeType.HIDDEN:
                color_map.append('blue')
            else:
                color_map.append("red")

        for link in self.links:
            graph.add_edge(link.from_node, link.to_node)


        positioning = nx.spring_layout(graph)
        nx.draw(graph, pos=positioning, edge_color='black', arrowsize=10, node_color=color_map)
        plt.show()

    def output_inactive(self):

        if self.running:
            return False

        else:
            output_nodes = self.nodes[self.num_inputs:self.num_inputs+self.num_outputs]
            for node in output_nodes:
                if node.activation_count == 0:
                    return True

            self.running = True
            return False

    def get_outputs(self):
        output_nodes = self.nodes[self.num_inputs:self.num_inputs+self.num_outputs]
        return [node.output for node in output_nodes]
