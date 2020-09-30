from random import random

class Breeder:


    def crossover(self, mother, father):
        """ Create offspring genome.

        Precondition:
            Link genes of the genomes are sorted with increasing innovation numbers.
            Link genes of the genomes are not None.

        Returns:
            Offspring genome.
        """

        offspring_nodes = set()
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
                better_link = better_genome[better_genome_index]
                worse_link = worse_genome[worse_genome_index]

                # If the links have the same innovation number, inherit randomly.
                if better_link.innovation_number == worse_link.innovation_number:

                    if random() < 0.5:
                        selected_link = better_link

                    else:
                        selected_link = worse_link

                    better_genome_index += 1
                    worse_genome_index += 1

                # Skip worse links that are disjoint.
                elif better_link.innovation_number > worse_link.innovation_number:
                    worse_genome_index += 1
                    continue

                # Inherit better links that are disjoint.
                elif better_link.innovation_number < worse_link.innovation_number:
                    selected_link = better_link
                    better_genome_index += 1

            offspring_nodes.append(selected_link)
            offspring_nodes.add(selected_link.from_node)
            offspring_nodes.add(selected_link.to_node)

        return offspring_links

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
            better_genome = father
            worse_genome = mother

        return better_genome, worse_genome
