from random import random
from neat.genome import Genome
from neat.link_gene import LinkGene
from neat.node_gene import NodeGene
from neat.enums.node_types import NodeType


class Breeder:
    """Create a new genome from two parent genomes by crossover. """

    def __init__(self, config):
        self.config = config
        self.genome_id = self.config.population_size - 1

    def crossover(self, mother, father, averaging):
        """ Create offspring genome.

        Precondition:
            Link genes of the genomes are sorted with increasing innovation numbers.
            Link genes of the genomes are not None.

        Returns:
            Offspring genome.
        """

        offspring_links = []

        better_genome, worse_genome = self.fitness_order(mother, father)
        better_genome_index = 0
        worse_genome_index = 0

        while better_genome_index < better_genome.size():

            # Only inherit excess links from the better genome.
            if worse_genome_index == worse_genome.size():
                selected_link = better_genome.links[better_genome_index]
                better_genome_index += 1

            else:
                better_link = better_genome.links[better_genome_index]
                worse_link = worse_genome.links[worse_genome_index]

                if better_link.id == worse_link.id:

                    # Either inherit averaged or random link.
                    if averaging:
                        selected_link = self.average_link(better_link, worse_link)
                    else:
                        if random() < 0.5:
                            selected_link = better_link
                        else:
                            selected_link = worse_link

                    better_genome_index += 1
                    worse_genome_index += 1

                # Skip worse links that are disjoint.
                elif better_link.id > worse_link.id:
                    worse_genome_index += 1
                    continue

                # Inherit better links that are disjoint.
                elif better_link.id < worse_link.id:
                    selected_link = better_link
                    better_genome_index += 1

            offspring_links.append(selected_link)

        new_genome = self.create_genome(offspring_links, mother.tracker)

        return new_genome


    def fitness_order(self, mother, father):
        """ Determine which is the fittest genome.

        The shortest genome is better if the genomes are of equal fitness.

        Args:
            mother: instance of neat.genome.Genome
            father: instance of neat.genome.Genome

        Returns:
            (better_genome, worse_genome)
        """
        if mother.fitness == father.fitness:

            if mother.size() < father.size():
                better_genome = mother
                worse_genome = father

            else:
                better_genome = father
                worse_genome = mother

        elif mother.fitness < father.fitness:
            better_genome = father
            worse_genome = mother


        else:
            better_genome = mother
            worse_genome = father

        return better_genome, worse_genome

    def create_genome(self, offspring_links, tracker, genome_id=None):
        """Create a new genome from the selected links.
           The links reference different node objects, so this function
           creates new links which reference the same new node objects.
        """
        copied_nodes = {}
        copied_links = []

         # The bias node must be saved, even if there are no links from it.
        found_bias = False

        for link in offspring_links:

            if link.from_node.type == NodeType.BIAS:
                found_bias = True

            if link.from_node.id not in copied_nodes.keys():
                copied_nodes[link.from_node.id] = link.from_node.copy()

            if link.to_node.id not in copied_nodes.keys():
                copied_nodes[link.to_node.id] = link.to_node.copy()

            from_node_copy = copied_nodes[link.from_node.id]
            to_node_copy = copied_nodes[link.to_node.id]
            link_copy = link.copy(from_node_copy, to_node_copy)

            copied_links.append(link_copy)

        copied_nodes = list(copied_nodes.values())

        # Create a bias node if it was not present in any of the links.
        if not found_bias:
            copied_nodes.append(NodeGene(NodeType.BIAS, 0, 0))

        # Ensure the nodes are sorted as expected [bias, input, output, hidden].
        copied_nodes = self.sort_nodes(copied_nodes)

        if genome_id is None:
            genome_id = self.genome_id
            self.genome_id += 1
        offspring = Genome(genome_id, self.config, copied_nodes, copied_links, tracker)

        return offspring

    def sort_nodes(self, nodes):
        """Sort nodes by types as [bias, input, output, hidden]. """
        bias = []
        inputs = []
        outputs = []
        hidden = []

        for node in nodes:
            if node.type == NodeType.BIAS:
                bias.append(node)

            elif node.type == NodeType.INPUT:
                inputs.append(node)

            elif node.type == NodeType.OUTPUT:
                outputs.append(node)

            elif node.type == NodeType.HIDDEN:
                hidden.append(node)

        return bias + inputs + outputs + hidden

    def average_link(self, link1, link2):
        new_weight = (link1.weight + link2.weight)/2

        from_node = link1.from_node.copy()
        to_node = link1.to_node.copy()
        enabled = link1.enabled
        recurrent = link1.recurrent

        new_link = LinkGene(from_node, to_node, enabled, recurrent)
        new_link.id = link1.id
        new_link.weight = new_weight

        return new_link
