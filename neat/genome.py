from random import random
from random import choice
from enums.node_types import NodeType

class Genome:

    def __init__(self, id, num_inputs, num_outputs):
        self.id = id
        self.nodes = []
        self.links = []
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

    def mutate_add_link(self, loop_probability, loop_tries, add_tries):
        """
        Mutate genome by adding a new link between two previously unconnected nodes.
        Returns None if the addition failed. Otherwise the new link gene.
        Pre: self.nodes begins with the input nodes.
        """

        # TODO: add non-loop recurrent links.
        if random() < loop_probability:

            while loop_tries:
                node = choice(self.nodes)

                if node.can_have_loop():
                    node.recurrent = True
                    # TODO: create gene and add to genome.
                    return node

                loop_tries -= 1

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

