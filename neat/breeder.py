from random import random
from neat.node_gene import NodeGene
from neat.genome import Genome


class Breeder:


    def crossover(self, mother, father):
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

        while(better_genome_index < better_genome.size()):

            # Only inherit excess links from the better genome.
            if worse_genome_index == worse_genome.size():
                selected_link = better_genome.links[better_genome_index]
                better_genome_index += 1

            else:
                better_link = better_genome.links[better_genome_index]
                worse_link = worse_genome.links[worse_genome_index]

                # Inherit matching links randomly.
                if better_link.id == worse_link.id:

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

        offspring_nodes = self.update_nodes(offspring_links)
        return Genome(mother.id, mother.num_inputs, mother.num_outputs, offspring_nodes, offspring_links)

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

    def update_nodes(self, offspring_links):
        """Create new nodes and update references in offspring links. """
        created_nodes = {}

        for link in offspring_links:

            if link.from_node.id not in created_nodes.keys():
                new_node = link.from_node.copy()
                created_nodes[link.from_node.id] = new_node
                link.from_node = new_node
            
            else:
                link.from_node = created_nodes[link.from_node.id]

            if link.to_node.id not in created_nodes.keys():
                new_node = link.to_node.copy()
                created_nodes[link.to_node.id] = new_node
                link.to_node = new_node

            else:
                link.to_node = created_nodes[link.to_node.id]

        offspring_nodes = list(created_nodes.values())
        return offspring_nodes
