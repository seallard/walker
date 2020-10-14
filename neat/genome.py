from random import random, uniform
from random import choice
from neat.enums.node_types import NodeType
from neat.link_gene import LinkGene
from neat.link import Link
from neat.node_gene import NodeGene
from neat.node import Node
from neat.network import Network


class Genome:

    def __init__(self, id, config, node_genes=None, link_genes=None):
        self.id = id
        self.config = config
        self.fitness = 0
        self.adjusted_fitness = 0
        self.phenotype = None

        if link_genes is None or node_genes is None:
            self.__initialise_nodes()
            self.__initialise_links()
        else:
            self.nodes = node_genes
            self.links = link_genes

    def mutate_add_link(self, tracker):
        """
        Mutate genome by adding a new link between two previously unconnected nodes.
        Returns None if the addition failed. Otherwise the new link gene.
        Pre: self.nodes begins with the input nodes.
        """

        if random() < self.config.loop_add_rate:
            return self.add_loop(tracker)

        return self.add_non_loop_link(tracker)

    def add_loop(self, tracker):
        """
        Add recurrent loop.
        Side effects: adds link gene to this genome.
                      sets recurrent attribute of node to True.
        """
        tries = self.config.loop_add_tries
        while tries:
            node = choice(self.nodes)

            if node.can_have_loop():
                node.recurrent = True
                new_gene = LinkGene(node, node, True, True)
                self.links.append(new_gene)
                tracker.assign_link_id(new_gene)
                return

            tries -= 1

    def add_non_loop_link(self, tracker):
        """
        Add non-loop link to genome.
        Side effects: adds link gene to this genome.
        """
        tries = self.config.link_add_tries
        while tries:
            from_node = choice(self.nodes)
            to_node = choice(self.nodes[self.config.num_inputs:])

            if self.invalid_link(from_node, to_node):
                tries -= 1
                continue

            recurrent = to_node.depth - from_node.depth <= 0
            new_gene = LinkGene(from_node, to_node, recurrent=recurrent)
            self.links.append(new_gene)
            tracker.assign_link_id(new_gene)
            return

    def invalid_link(self, from_node, to_node):
        link_exists = self.link_exists(from_node, to_node)
        both_are_outputs = from_node.is_output() and to_node.is_output()
        same_nodes = from_node.id == to_node.id

        return (
            link_exists or
            same_nodes or
            both_are_outputs or
            not to_node.valid_out()
        )

    def mutate_add_node(self, tracker):
        """
        Random insertion of a node between two previously connected nodes.

        Side effects (if valid link is found):
            - disables link
            - appends one node gene and two link genes to this genome
        """
        tries = self.config.node_add_tries
        while tries:
            biased_index = round(abs(random() - random())*(len(self.links)-1))
            link = self.links[biased_index]

            if not link.can_be_split():
                tries -= 1
                continue

            link.enabled = False

            depth = abs(link.to_node.depth - link.from_node.depth)/2
            new_node = NodeGene(NodeType.HIDDEN, depth)
            new_in_link = LinkGene(link.from_node, new_node)
            new_out_link = LinkGene(new_node, link.to_node)

            new_in_link.weight = 1
            new_out_link.weight = link.weight

            self.nodes.append(new_node)
            self.links.append(new_in_link)
            self.links.append(new_out_link)

            tracker.assign_node_id(link.from_node.id, link.to_node.id, new_node)
            tracker.assign_link_id(new_in_link)
            tracker.assign_link_id(new_out_link)
            return

    def mutate_weights(self):
        """Perturb or replace weights.
        """
        for link in self.links:

            if random() > self.config.weight_mutation_rate:
                continue

            if random() < self.config.weight_replacement_rate:
                link.weight = uniform(-1, 1)

            else:
                link.weight += uniform(-1, 1) * self.config.weight_mutation_range

    def link_exists(self, from_node, to_node):
        """Check if link is present in the genome. """

        for link in self.links:
            if link.from_node.id == from_node.id and link.to_node.id == to_node.id:
                return True
        return False

    def __initialise_nodes(self):
        """Create the input and output genes. """
        self.nodes = []
        in_depth = 0
        out_depth = 1

        for innovation_number in range(self.config.num_inputs):
            node = NodeGene(NodeType.INPUT, in_depth, innovation_number)
            self.nodes.append(node)

        for innovation_number in range(self.config.num_inputs, self.config.num_inputs + self.config.num_outputs):
            node = NodeGene(NodeType.OUTPUT, out_depth, innovation_number)
            self.nodes.append(node)

    def __initialise_links(self):
        """Connect each input node to each output node. """
        self.links = []
        innovation_number = 0
        for input_node in self.nodes[:self.config.num_inputs]:
            for output_node in self.nodes[self.config.num_inputs:]:
                link = LinkGene(input_node, output_node)
                link.id = innovation_number
                self.links.append(link)
                innovation_number += 1


    def size(self):
        return len(self.links)

    def network(self):
        """Create and return network phenotype of genome. """

        nodes = {}

        for node_gene in self.nodes:
            nodes[node_gene.id] = Node(node_gene)

        links = []

        for link_gene in self.links:

            if link_gene.enabled:
                from_node = nodes[link_gene.from_node.id]
                to_node = nodes[link_gene.to_node.id]

                # Create link.
                link = Link(from_node, to_node, link_gene.weight)
                links.append(link)

                # Update in and out links of nodes.
                from_node.out_links.append(link)
                to_node.in_links.append(link)

        nodes = list(nodes.values())
        network = Network(nodes, links, self.config.num_inputs, self.config.num_outputs)
        self.phenotype = network
        return network
