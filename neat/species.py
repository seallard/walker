from random import choice
from math import floor
from random import random


class Species:

    def __init__(self, id, first_genome, config, breeder):
        self.id = id
        self.leader = first_genome
        self.genomes = [first_genome]
        self.age_since_improvement = 0
        self.age = 0
        self.expected_offspring = 0
        self.config = config
        self.breeder = breeder

    def add_genome(self, new_genome):

        added_genome = False

        for i, genome in enumerate(self.genomes):

            if new_genome.fitness > genome.fitness:
                self.genomes[i:i] = [new_genome]
                added_genome = True
                break

        if not added_genome:
            self.genomes.append(new_genome)

        if new_genome.fitness > self.leader.fitness:
            self.leader = new_genome
            self.age_since_improvement = 0

    def epoch_reset(self):
        self.genomes = []
        self.age += 1
        self.age_since_improvement += 1
        self.expected_offspring = 0

    def should_go_extinct(self):
        return self.age_since_improvement > self.config.maximum_stagnation

    def reproduce(self):

        offspring = []

        if self.genomes == []:
            return []

        # Always save species leader as is.
        offspring.append(self.breeder.create_genome(self.leader.links, self.leader.tracker))

        best_percent_index = floor(self.config.survival_threshold*len(self.genomes))
        mating_pool = self.genomes[:best_percent_index]

        while len(offspring) < self.expected_offspring:

            # Some of the time, only mutate.
            if random() <= self.config.mutate_only_probability or mating_pool == []:

                # Choose the random parent.
                if mating_pool == []:
                    parent = self.genomes[0]

                else:
                    parent = choice(mating_pool)

                copy = self.breeder.create_genome(parent.links, parent.tracker)

                structural_mutation_succeeded = copy.mutate_structure()

                if not structural_mutation_succeeded:
                    copy.mutate_non_structure()

                offspring += [copy]

            # Some of the time, mate.
            else:
                mother = choice(mating_pool)
                father = choice(mating_pool)

                # Decide if matching links should be averaged or inherited randomly.
                averaging = random() < self.config.mate_by_averaging

                baby = self.breeder.crossover(mother, father, averaging)
                offspring.append(baby)

        return offspring

    def get_average_fitness(self):

        if self.genomes == []:
            return 0

        total_fitness = self.get_total_fitness()
        return total_fitness/len(self.genomes)

    def get_total_fitness(self):
        total_fitness = 0
        for genome in self.genomes:
            total_fitness += genome.fitness
        return total_fitness
