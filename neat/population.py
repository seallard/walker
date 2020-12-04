from neat.genome import Genome
from neat.species import Species
from neat.innovation_tracker import InnovationTracker
from neat.breeder import Breeder
from math import floor
from random import random
from random import choice


class Population:

    def __init__(self, config):
        self.config = config
        self.species = []
        self.species_id = 0
        self.genomes = []
        self.tracker = InnovationTracker(config)
        self.breeder = Breeder(config)
        self.generation = 0

        for i in range(config.population_size):
            genome = Genome(i, config, tracker=self.tracker)
            self.genomes.append(genome)

    def speciate_genomes(self):
        """Place each genome into a species. """
        for genome in self.genomes:
            species_found = False

            for species in self.species:
                compatibility = genome.compatibility(species.leader)

                if compatibility < self.config.compatibility_threshold:
                    species.add_genome(genome)
                    species_found = True
                    break

            if not species_found:
                new_species = Species(self.species_id, genome, self.config, self.breeder)
                self.species.append(new_species)
                self.species_id += 1

    def set_spawn_amounts(self):
        """Fitness sharing. """

        # Sort by decreasing fitness.
        self.species.sort(key=lambda x: x.leader.original_fitness, reverse=True)

        non_stagnated_species = [species for species in self.species if not species.stagnated()]

        # When all species stagnate, only let the two best reproduce.
        if len(non_stagnated_species) == 0:
            self.species = self.species[:2]

        # Offspring = (AverageSpeciesFitness / Total_of_AverageSpeciesFitnesss) * PopulationSize
        total_average_species_fitness = 0
        for species in self.species:
            total_average_species_fitness += species.get_average_fitness()

        remainder = 0

        for species in self.species:

            average_species_fitness = species.get_average_fitness()
            offspring = (average_species_fitness/total_average_species_fitness) * self.config.population_size

            species.expected_offspring = int(offspring)

            # Deal with fractional remainder of expected offspring.
            remainder += offspring - int(offspring)

            if remainder > 1:
                remainder_int = floor(remainder)
                species.expected_offspring += remainder_int
                remainder -= remainder_int

        # Check if any precision was lost.
        total_expected_offspring = 0
        for species in self.species:
            total_expected_offspring += species.expected_offspring

        if total_expected_offspring < self.config.population_size:
            self.species[0].expected_offspring += 1

    def reproduce(self):
        new_population = []
        for species in self.species:

            do_interspecies_mating = False

            if floor(len(species.genomes) * self.config.survival_threshold) > 0:
                interspecies_matings = self.number_of_interspecies_matings(species)
                species.expected_offspring -= interspecies_matings
                do_interspecies_mating = True

            if species.expected_offspring > 0:
                new_population += species.reproduce()

            if do_interspecies_mating:
                for i in range(interspecies_matings):
                    mother = choice(self.species).leader
                    father = species.get_random_parent()
                    averaging = random() < self.config.mate_by_averaging

                    offspring = self.breeder.crossover(mother, father, averaging)
                    new_population.append(offspring)

        self.genomes = new_population

    def number_of_interspecies_matings(self, species):
        counter = 0
        for i in range(species.expected_offspring):
            if random() < self.config.interspecies_mating_rate:
                counter += 1
        return counter

    def stopping_criterion(self):
        return False

    def reset(self):

        # Remove empty species.
        self.species = [species for species in self.species if not species.is_empty()]

        if self.config.dynamic_thresholding:

            # Adjust the compatibility threshold.
            if len(self.species) < self.config.target_number_of_species:
                self.config.compatibility_threshold -= self.config.threshold_adjustment

            if len(self.species) > self.config.target_number_of_species:
                self.config.compatibility_threshold += self.config.threshold_adjustment

            if self.config.compatibility_threshold < self.config.threshold_adjustment:
                self.config.compatibility_threshold = self.config.threshold_adjustment

        for species in self.species:
            species.epoch_reset()

        self.generation += 1

    def adjust_negative_fitness_scores(self):
        """Shift all fitness scores so that they are positive.
           Only necessary if the fitness function used can assign negative scores.
        """

        # Find the lowest fitness value.
        min_fitness = self.genomes[0].original_fitness
        for genome in self.genomes:
            if genome.original_fitness < min_fitness:
                min_fitness = genome.original_fitness

        if min_fitness > 0:
            return

        for genome in self.genomes:
            genome.original_fitness += abs(min_fitness)

    def adjust_fitness_scores(self):
        """Boost young and penalise old species. """

        for species in self.species:
            species.adjust_fitness()

    def run(self, fitness_function, use_novelty, weighting, n=None, run=None):
        """Run NEAT for n generations or until solution is found. """

        solution_found = False

        while self.generation < n and not solution_found:

            print(f"Generation {self.generation} of 500 in run {run} of 30")

            # Assign fitness scores. TODO: fix parameter forwarding.
            solution_found = fitness_function(self.genomes, use_novelty, weighting)

            # Terminate if solution was found.
            if solution_found:
                return True

            self.speciate_genomes()
            self.set_spawn_amounts()
            self.reproduce()
            self.reset()
