from neat.genome import Genome
from neat.species import Species
from neat.innovation_tracker import InnovationTracker
from neat.breeder import Breeder
from math import floor


class Population:

    def __init__(self, config):
        self.config = config
        self.species = []
        self.species_id = 0
        self.genomes = []
        self.tracker = InnovationTracker(config)
        self.breeder = Breeder(config)

        for i in range(config.population_size):
            genome = Genome(i, config)
            self.genomes.append(genome)

    def speciate_genomes(self):
        """Place each genome into a species. """
        for genome in self.genomes:
            species_found = False

            for species in self.species:
                compatibility = self.compatibility(genome, species.leader)

                if compatibility < self.config.compatibility_threshold:
                    species.add_member(genome)
                    species_found = True
                    break

            if not species_found:
                new_species = Species(self.species_id, genome, self.config)
                self.species.append(new_species)
                self.species_id += 1

    def compatibility(self, g1, g2):
        """Compatibility of genomes. """

        weight_diff = 0
        matched = 0
        disjoint = 0
        excess = 0

        g1_index = 0
        g2_index = 0

        while g1_index <= g1.size():

            # Reached end of g2.
            if g2_index == g2.size():
                excess += len(g1.links) - g1_index
                break

            # Reached end of g1.
            if g1_index == g1.size():
                excess += len(g2.links) - g2_index
                break

            g1_gene = g1.links[g1_index]
            g2_gene = g2.links[g2_index]

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

        if g1.size() > g2.size():
            n = g1.size()

        else:
            n = g2.size()

        disjoint = self.config.c_disjoint * disjoint/n
        excess = self.config.c_excess * excess/n
        weight = self.config.c_weight * weight_diff/matched

        return disjoint + excess + weight

    def set_spawn_amounts(self):
        total_population_fitness = self.total_fitness()
        for species in self.species:
            fitness = species.average_adjusted_fitness()
            offspring = floor(fitness/total_population_fitness)
            species.expected_offpsring = offspring

    def total_fitness(self):
        total_fitness = 0
        for species in self.species:
            total_fitness += species.average_adjusted_fitness()
        return total_fitness

    def reproduce(self):
        new_population = []

        for species in self.species:
            new_population += species.reproduce()

    def mutate(self):
        for genome in self.genomes:
            genome.mutate_weights()
            genome.mutate_add_link(self.tracker)
            genome.mutate_add_node(self.tracker)

    def stopping_criterion(self):
        return False

    def reset(self):
        for species in self.species:
            species.epoch_reset()

    def adjust_fitness_scores(self):
        for species in self.species:
            species.adjust_fitness()
