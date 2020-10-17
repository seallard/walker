from random import random, uniform
from random import choice
from neat.enums.node_types import NodeType
from neat.link_gene import LinkGene
from neat.link import Link
from neat.node_gene import NodeGene
from neat.node import Node
from neat.network import Network


class Genome:

    def __init__(self, id, config, node_genes=None, link_genes=None, tracker=None):
        self.id = id
        self.config = config
        self.fitness = 0
        self.adjusted_fitness = 0
        self.phenotype = None
        self.tracker = tracker

        if link_genes is None or node_genes is None:
            self.__initialise_nodes()
            self.__initialise_links()
        else:
            self.nodes = node_genes
            self.links = link_genes

    def mutate_structure(self):
        """Call each method of structural mutation with a certain probability. """

        if random() < self.config.add_node_probability:
            return self.mutate_add_node()

        if random() < self.config.add_link_probability:
            return self.mutate_add_link()

    def mutate_non_structure(self):
        """Call each method of non-structural mutation with a certain probability. """

        if random() < self.config.weight_mutation_probability:
            self.mutate_weights()

        if random() < self.config.link_reenable_probability:
            self.mutate_reenable_link()

        if random() < self.config.link_toggle_enabled_probability:
            self.mutate_toggle_enable()

    def mutate_add_link(self):
        """
        Mutate genome by adding a new link between two previously unconnected nodes.
        The added link is either forward, recurrent or a loop.
        Pre: self.nodes begins with the input nodes.
        """

        if random() < self.config.recurrent_probability:

            if random() < 0.5:
                return self.add_loop_link()

            else:
                return self.add_recurrent_link()

        else:
            return self.add_forward_link()

    def add_loop_link(self):
        """
        Add recurrent loop.
        Side effects: adds link gene to this genome.
                      sets recurrent attribute of node to True.
        """
        tries = self.config.link_add_tries
        while tries:
            node = choice(self.nodes)

            if node.can_have_loop() and not self.link_exists(node, node):
                new_gene = LinkGene(node, node, recurrent=True)
                self.tracker.assign_link_id(new_gene)
                self.insert_link(new_gene)
                print("Added a loop link")
                return True
            tries -= 1

    def add_recurrent_link(self):
        tries = self.config.link_add_tries
        while tries:
            from_node = choice(self.nodes)
            to_node = choice(self.nodes[self.config.num_inputs:])

            if self.invalid_recurrent_link(from_node, to_node):
                tries -= 1
                continue

            new_gene = LinkGene(from_node, to_node, recurrent=True)
            self.tracker.assign_link_id(new_gene)
            self.insert_link(new_gene)
            return True

    def invalid_recurrent_link(self, from_node, to_node):
        link_exists = self.link_exists(from_node, to_node)
        is_forward = from_node.depth - to_node.depth <= 0

        return (
            link_exists or
            not to_node.valid_out() or
            is_forward
        )

    def add_forward_link(self):
        """
        Add forward link to genome.
        Side effects: adds link gene to this genome.
        """
        tries = self.config.link_add_tries
        while tries:
            from_node = choice(self.nodes)
            to_node = choice(self.nodes[self.config.num_inputs:])

            if self.invalid_forward_link(from_node, to_node):
                tries -= 1
                continue

            new_gene = LinkGene(from_node, to_node, recurrent=False)
            self.tracker.assign_link_id(new_gene)
            self.insert_link(new_gene)
            return True

    def invalid_forward_link(self, from_node, to_node):
        link_exists = self.link_exists(from_node, to_node)
        is_backward = from_node.depth - to_node.depth >= 0

        return (
            link_exists or
            not to_node.valid_out() or
            is_backward
        )

    def mutate_add_node(self):
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

            if not link.can_be_split() or self.link_split_before(link):
                tries -= 1
                continue

            link.enabled = False

            depth = abs(link.to_node.depth - link.from_node.depth)/2

            new_node = NodeGene(NodeType.HIDDEN, depth)
            new_in_link = LinkGene(link.from_node, new_node)
            new_out_link = LinkGene(new_node, link.to_node)

            new_in_link.weight = 1
            new_out_link.weight = link.weight

            self.tracker.assign_node_id(link.from_node.id, link.to_node.id, new_node)
            self.tracker.assign_link_id(new_in_link)
            self.tracker.assign_link_id(new_out_link)

            self.nodes.append(new_node)
            self.insert_link(new_in_link)
            self.insert_link(new_out_link)
            print("Added a node")

            return True

    def link_split_before(self, link):
        """Checks whether a node exists between the two nodes in the link. """

        from_node = link.from_node
        to_node = link.to_node

        for in_link in self.links:
            if in_link.from_node == from_node:

                for out_link in self.links:
                    if out_link.from_node == in_link.to_node and out_link.to_node == to_node:
                        return True

    def mutate_reenable_link(self):
        """Find the first disabled link and reenable it. """
        for link in self.links:
            if not link.enabled:
                link.enabled = True
                return

    def mutate_toggle_enable(self):
        """Toggle a random links enabled property if safe to do so. """
        link = choice(self.links)

        if self.safe_to_toggle(link):
            link.enabled = not link.enabled

    def safe_to_toggle(self, toggle_link):
        """Make sure it is safe to toggle the link. Some valid toggles are discarded
           since they are difficult to verify as safe.
        """
        if not toggle_link.enabled:
            return True

        for link in self.links:
            same_from_node = link.from_node == toggle_link.from_node
            if link != toggle_link and link.enabled and same_from_node and not link.recurrent:
                return True

    def mutate_weights(self):
        """Perturb or replace weights.
        """
        for link in self.links:

            if random() > self.config.weight_mutation_probability:
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


    def insert_link(self, link_gene):
        """Maintain links sorted by increasing innovation numbers.
        """

        if self.links and link_gene.id > self.links[-1].id:
            self.links.append(link_gene)
            return

        for i, link in enumerate(self.links):

            if link.id > link_gene.id:
                self.links[i:i] = [link_gene] # Insert link at index i.
                return

        self.links.append(link_gene)
