import networkx as nx
import matplotlib.pyplot as plt
from neat.enums.node_types import NodeType


class Network:

    def __init__(self, nodes, links):
        self.nodes = nodes
        self.links = links

    def update(self, inputs):
        """Propagate signals one node forward in the network. """

        # Initialise input nodes with inputs.
        for i, node in enumerate(self.nodes[:self.num_inputs]):
            node.output = inputs[i]

        outputs = []

        for node in self.nodes[self.num_inputs:]:
            node.activate()

            if node.is_output():
                outputs.append(node.output)

        return outputs

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
        nx.draw(graph, pos=positioning, edge_color='black', arrowsize=5, arrowstyle='fancy', node_color=color_map)
        plt.show()
