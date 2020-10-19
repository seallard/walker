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
            genome = Genome(i, config, tracker=self.tracker)
            self.genomes.append(genome)

    def speciate_genomes(self):
        """Place each genome into a species. """
        for genome in self.genomes:
            species_found = False

            for species in self.species:
                compatibility = self.compatibility(genome, species.leader)

                if compatibility < self.config.compatibility_threshold:
                    species.add_genome(genome)
                    species_found = True
                    break

            if not species_found:
                new_species = Species(self.species_id, genome, self.config, self.breeder)
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
        """Fitness sharing. """

        # Offspring = (AverageSpeciesFitness / Total_of_AverageSpeciesFitnesss) * PopulationSize
        total_fitness = 0
        for species in self.species:
            total_fitness += species.get_total_fitness()

        average_total_fitness = total_fitness/len(self.genomes)

        for species in self.species:
            average_species_fitness = species.get_average_fitness()
            offspring = (average_species_fitness/average_total_fitness) * len(self.genomes)
            species.expected_offspring = offspring

    def reproduce(self):
        new_population = []
        for species in self.species:
            new_population += species.reproduce()

        self.genomes = new_population

    def stopping_criterion(self):
        return False

    def reset(self):
        self.species = [species for species in self.species if not species.should_go_extinct()]
        for species in self.species:
            species.epoch_reset()

    def calculate_mean_adjusted_fitness(self):
        """Mean adjusted fitness of the entire population. """
        total = 0
        for species in self.species:
            total += species.adjusted_sum
        return total/len(self.species)

    def statistics(self):
        print(f"Number of species in population: {len(self.species)}")
        print(f"Number of genomes in population: {len(self.genomes)}")

    def adjust_negative_fitness_scores(self):
        """Shift all fitness scores so that they are positive.
           Only necessary if the fitness function used can assign negative scores.
        """

        # Find the lowest fitness value.
        min_fitness = self.genomes[0].fitness
        for genome in self.genomes:
            if genome.fitness < min_fitness:
                min_fitness = genome.fitness

        if min_fitness > 0:
            return

        for genome in self.genomes:
            genome.fitness += abs(min_fitness)
