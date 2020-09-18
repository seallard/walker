from random import random
from random import choice
from neat.enums.node_types import NodeType
from neat.link_gene import LinkGene
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

        if random() < loop_probability:
            return self.add_loop(loop_tries)

        return self.add_non_loop_link(add_tries)

    def add_loop(self, tries):
        """
        Add recurrent loop.
        Returns None if failed. Otherwise a link gene.
        Side effects: adds link gene to this genome.
                      sets recurrent attribute of node to True.
        """

        while tries:
            node = choice(self.nodes)

            if node.can_have_loop():
                node.recurrent = True
                new_gene = LinkGene(node, node, True, True)
                self.links.append(new_gene)
                return new_gene

            tries -= 1

    def add_non_loop_link(self, tries):
        """
        Add non-loop link to genome.
        Returns None if failed. Otherwise a link gene.
        Side effects: adds link gene to this genome.
        """
        while tries:
            from_node = choice(self.nodes)
            to_node = choice(self.nodes[self.num_inputs:])

            if self.__invalid_link(from_node, to_node):
                tries -= 1
                continue

            recurrent = to_node.depth - from_node.depth <= 0
            new_gene = LinkGene(from_node, to_node, recurrent=recurrent)
            self.links.append(new_gene)
            return new_gene

    def __invalid_link(self, from_node, to_node):
        link_exists = self.link_exists(from_node, to_node)
        both_are_outputs = from_node.is_output() and to_node.is_output()
        same_nodes = from_node.innovation_number == to_node.innovation_number

        return (
            link_exists or
            same_nodes or
            both_are_outputs or
            not to_node.valid_out()
        )

    def mutate_add_node(self, tries):
        """
        Random insertion of a node between two previously connected nodes.

        Side effects (if valid link is found):
            - disables link
            - appends one node gene and two link genes to this genome
        """

        while tries:
            # Distribute splitting evenly using bias towards older links.
            # TODO: Might be better to only use bias if genome is small.
            biased_index = round(abs(random() - random())*(len(self.links)-1))
            link = self.links[biased_index]

            if not link.can_be_split():
                tries -= 1
                continue

            link.enabled = False
            original_weight = link.weight
            original_from_node = link.from_node
            original_to_node = link.to_node

            depth = abs(original_to_node.depth - original_from_node.depth)/2
            new_node = NodeGene(NodeType.HIDDEN, depth)
            new_in_link = LinkGene(original_from_node, new_node)
            new_out_link = LinkGene(new_node, original_to_node)

            new_in_link.weight = 1
            new_out_link.weight = original_weight

            self.nodes.append(new_node)
            self.links.extend([new_in_link, new_out_link])

            return (new_node, new_in_link, new_out_link)

    def mutate_weights(self):
        """Perturb or replace weights. """
        pass

    def compatibility_score(self, other):
        """Calculate compatibility score with other genome. """
        pass

    def crossover(self, other):
        """Create a child genome. """
        pass

    def link_exists(self, from_node, to_node):
        """Check if link is present in the genome. """
        from_id = from_node.innovation_number
        to_id = to_node.innovation_number
        for link in self.links:
            if link.from_node.innovation_number == from_id and link.to_node.innovation_number == to_id:
                return True
        return False

    def duplicate_node(self, innovation_number):
        """Check if node is present in the genome. """
        pass

    def get_index_of_node(self, innovation_number):
        """Find index of node in the list of nodes. """
        pass

    def __initialise_nodes(self):
        """Create the input and output genes. """
        self.nodes = []
        in_depth = 0
        out_depth = 1

        for innovation_number in range(self.num_inputs):
            node = NodeGene(NodeType.INPUT, in_depth, innovation_number)
            self.nodes.append(node)

        for innovation_number in range(self.num_inputs, self.num_inputs + self.num_outputs):
            node = NodeGene(NodeType.OUTPUT, out_depth, innovation_number)
            self.nodes.append(node)

    def __initialise_links(self):
        """Connect each input node to each output node. """
        self.links = []
        innovation_number = self.num_inputs + self.num_outputs
        for input_node in self.nodes[:self.num_inputs]:
            for output_node in self.nodes[self.num_inputs:]:
                link = LinkGene(input_node, output_node)
                link.innovation_number = innovation_number
                self.links.append(link)
                innovation_number += 1
