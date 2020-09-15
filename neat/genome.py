from random import random
from random import choice
from neat.enums.node_types import NodeType
from neat.connection_gene import ConnectionGene
from neat.node_gene import NodeGene

class Genome:

    def __init__(self, id, num_inputs, num_outputs):
        self.id = id
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.__initialise_nodes()
        self.__initialise_links()

    def mutate_add_link(self, loop_probability, loop_tries, add_tries):
        """
        Mutate genome by adding a new link between two previously unconnected nodes.
        Returns None if the addition failed. Otherwise the new link gene.
        Pre: self.nodes begins with the input nodes.
        """

        # TODO: add non-loop recurrent links.
        if random() < loop_probability:
            return self.add_loop(loop_tries)

        else:

            while add_tries:
                from_node = choice(self.nodes)
                to_node = choice(self.nodes[self.num_inputs:]) # Non-input node.

                if not to_node.can_be_out_node():
                    add_tries -= 1
                    continue

                link_exists = self.link_exists(from_node.id, to_node.id)

                if not link_exists and from_node.id != to_node.id:
                    # TODO: create gene and add to genome.
                    return (from_node, to_node)

    def add_loop(self, tries):
        """
        Add recurrent loop.
        Returns None if failed. Otherwise a connection gene.
        Side effects: adds connection gene to this genome.
                      sets recurrent attribute of node to True.
        """

        while tries:
            node = choice(self.nodes)

            if node.can_have_loop():
                node.recurrent = True
                new_gene = ConnectionGene(node, node, True, True)
                self.links.append(new_gene)
                return new_gene

            tries -= 1

    def add_non_recurrent_link(self):
        pass

    def mutate_add_node(self):
        """Random insertion of a node between two previously connected nodes. """
        pass

    def mutate_weights(self):
        """Perturb or replace weights. """
        pass

    def compatibility_score(self, other):
        """Calculate compatibility score with other genome. """
        pass

    def crossover(self, other):
        """Create a child genome. """
        pass

    def link_exists(self, from_id, to_id):
        """Check if link is present in the genome. """
        for link in self.links:
            if link.from_node.id == from_id and link.to_node.id == to_id:
                return True
        return False

    def duplicate_node(self, node_id):
        """Check if node is present in the genome. """
        pass

    def get_index_of_node(self, node_id):
        """Find index of node in the list of nodes. """
        pass

    def __initialise_nodes(self):
        """Create the input and output genes. """
        self.nodes = []

        for node_id in range(self.num_inputs):
            node = NodeGene(NodeType.INPUT, node_id)
            self.nodes.append(node)

        for node_id in range(self.num_inputs, self.num_inputs + self.num_outputs):
            node = NodeGene(NodeType.OUTPUT, node_id)
            self.nodes.append(node)

    def __initialise_links(self):
        """Connect each input node to each output node. """
        self.links = []
        innovation_id = self.num_inputs + self.num_outputs
        for input_node in self.nodes[:self.num_inputs]:
            for output_node in self.nodes[self.num_inputs:]:
                link = ConnectionGene(input_node, output_node)
                link.innovation_id = innovation_id
                self.links.append(link)
                innovation_id += 1