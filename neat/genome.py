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
        self.original_fitness = 0
        self.fitness = 0
        self.tracker = tracker

        if link_genes is None or node_genes is None:
            self.__initialise_nodes()
            self.__initialise_links()
        else:
            self.nodes = node_genes
            self.links = link_genes

    def mutate_structure(self):
        """Call each method of structural mutation with a certain probability. """
        node_success = False
        link_success = False

        if random() < self.config.add_node_probability:
            node_success = self.mutate_add_node()

        if random() < self.config.add_link_probability:
            link_success = self.mutate_add_link()

        return node_success or link_success

    def mutate_non_structure(self):
        """Call each method of non-structural mutation with a certain probability. """

        self.mutate_weights() # Iterate over each link and mutate with some probability.

        if random() < self.config.reenable_link_probability:
            self.mutate_reenable_link()

        if random() < self.config.toggle_probability:
            self.mutate_toggle_enable()

    def mutate_add_link(self):
        """
        Mutate genome by adding a new link between two previously unconnected nodes.
        The added link is either forward, recurrent or a loop.
        Pre: self.nodes begins with the input nodes.
        """

        if random() < self.config.link_recurrent_probability:

            if random() > 0.5:
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

            # Select a random non-input node.
            node = choice(self.nodes[self.config.num_inputs+1:])

            if node.can_have_loop() and not self.link_exists(node, node):

                new_gene = LinkGene(node, node, recurrent=True)
                self.tracker.assign_link_id(new_gene)
                self.insert_link(new_gene)

                return True

            tries -= 1

    def add_recurrent_link(self):

        tries = self.config.link_add_tries

        while tries:

            from_node = choice(self.nodes[self.config.num_inputs+1:])
            to_node_pool = self.nodes[self.config.num_inputs + self.config.num_outputs+1:]

            # Might be impossible to add recurrent link.
            if to_node_pool == []:
                break

            to_node = choice(to_node_pool)

            if self.valid_recurrent_link(from_node, to_node):

                new_gene = LinkGene(from_node, to_node, recurrent=True)
                self.tracker.assign_link_id(new_gene)
                self.insert_link(new_gene)

                return True

            tries -= 1


    def valid_recurrent_link(self, from_node, to_node):
        link_exists = self.link_exists(from_node, to_node)
        is_recurrent = from_node.depth - to_node.depth > 0

        return (
            not link_exists and
            to_node.valid_out() and
            is_recurrent
        )

    def add_forward_link(self):
        """
        Add forward link to genome.
        Side effects: adds link gene to this genome.
        """

        inputs = self.nodes[:self.config.num_inputs + 1]
        hidden = self.nodes[self.config.num_inputs + 1 + self.config.num_outputs:]

        tries = self.config.link_add_tries

        while tries:

            from_node = choice(inputs + hidden)
            to_node = choice(self.nodes[self.config.num_inputs + 1:])

            if self.valid_forward_link(from_node, to_node):

                new_gene = LinkGene(from_node, to_node, recurrent=False)
                self.tracker.assign_link_id(new_gene)
                self.insert_link(new_gene)

                return True

            tries -= 1

    def valid_forward_link(self, from_node, to_node):
        link_exists = self.link_exists(from_node, to_node)
        is_forward = from_node.depth - to_node.depth < 0

        return (
            not link_exists and
            to_node.valid_out() and
            is_forward
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

            # Bias link index towards older ones to avoid chaining effect if few links exist.
            if len(self.nodes) < 10:
                biased_index = round(abs(random() - random())*(len(self.links)-1))
                link = self.links[biased_index]

            else:
                link = choice(self.links)

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

            # TODO: check whether node id is used in genome already.
            self.tracker.assign_node_id(link.from_node.id, link.to_node.id, new_node)
            self.tracker.assign_link_id(new_in_link)
            self.tracker.assign_link_id(new_out_link)

            self.nodes.append(new_node)
            self.insert_link(new_in_link)
            self.insert_link(new_out_link)

            return True

    def mutate_reenable_link(self):
        """Find the first disabled link and reenable it. """
        for link in self.links:
            if not link.enabled:
                link.enabled = True
                return

    def mutate_toggle_enable(self):
        """Toggle a random links enabled attribute. """
        link = choice(self.links)

        if self.safe_to_toggle(link):
            link.enabled = not link.enabled

    def safe_to_toggle(self, toggle_link):
        """
        Make sure there is another link from the from_node of the link being toggled.
        """
        if not toggle_link.enabled:
            return True

        for link in self.links:
            same_from_node = link.from_node == toggle_link.from_node

            if same_from_node and link.enabled and link != toggle_link:
                return True

    def mutate_weights(self):
        """Perturb or replace weights.
        """
        for link in self.links:

            # Mutate each link weight with some probability.
            if random() < self.config.weight_mutation_probability:

                # Some of the time, replace the weight entirely.
                if random() < self.config.weight_replacement_rate:
                    link.weight = uniform(-1, 1)

                # Otherwise, only perturb it by some small amount.
                else:
                    link.weight += uniform(-1, 1) * self.config.weight_mutation_power

            # Cap weights.
            if link.weight > 8.0:
                link.weight = 8.0

            if link.weight < -8.0:
                link.weight = -8.0

    def link_exists(self, from_node, to_node):
        """Check if link is present in the genome. """

        for link in self.links:
            if link.from_node.id == from_node.id and link.to_node.id == to_node.id:
                return True
        return False

    def __initialise_nodes(self):
        """Create the bias, input and output genes. """
        self.nodes = []
        in_depth = 0
        out_depth = 1

        bias_node = NodeGene(NodeType.BIAS, in_depth, 0)
        self.nodes.append(bias_node)

        for innovation_number in range(1, self.config.num_inputs+1):
            input_node = NodeGene(NodeType.INPUT, in_depth, innovation_number)
            self.nodes.append(input_node)

        for innovation_number in range(self.config.num_inputs+1, self.config.num_inputs + self.config.num_outputs + 1):
            output_node = NodeGene(NodeType.OUTPUT, out_depth, innovation_number)
            self.nodes.append(output_node)

    def __initialise_links(self):
        """Connect each input node (and bias) to each output node. """
        self.links = []

        for input_node in self.nodes[:self.config.num_inputs + 1]:
            for output_node in self.nodes[self.config.num_inputs + 1:]:
                link = LinkGene(input_node, output_node)
                self.tracker.assign_link_id(link)
                self.links.append(link)

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
                link = Link(from_node, to_node, link_gene.weight, link_gene.id)
                links.append(link)

                # Add link to nodes.
                from_node.out_links.append(link)
                to_node.in_links.append(link)

        nodes = list(nodes.values()) # Already sorted correctly [bias, inputs, outputs, hidden]
        network = Network(nodes, links, self.config.num_inputs, self.config.num_outputs)
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


    def compatibility(self, other):
        """Compatibility score. """

        weight_diff = 0
        matched = 0
        disjoint = 0
        excess = 0

        g1_index = 0
        g2_index = 0

        self_size = self.size()
        other_size = other.size()

        while g1_index <= self_size:

            # Reached end of other.
            if g2_index == other_size:
                excess += len(self.links) - g1_index
                break

            # Reached end of self.
            if g1_index == self_size:
                excess += len(other.links) - g2_index
                break

            g1_gene = self.links[g1_index]
            g2_gene = other.links[g2_index]

            if g2_gene.id == g1_gene.id:
                matched += 1
                weight_diff += abs(g2_gene.weight - g1_gene.weight)
                g2_index += 1
                g1_index += 1

            elif g2_gene.id > g1_gene.id:
                disjoint += 1
                g1_index += 1

            else:
                disjoint += 1
                g2_index += 1

        disjoint = self.config.c_disjoint * disjoint
        excess = self.config.c_excess * excess
        weight = self.config.c_weight * weight_diff/matched

        return disjoint + excess + weight