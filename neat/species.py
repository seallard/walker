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
        self.adjusted_sum = 0
        self.breeder = breeder

    def adjust_fitness(self):

        for genome in self.genomes:

            fitness = genome.fitness

            if self.age < self.config.young_boost:
                fitness *= self.config.young_boost

            if self.age > self.config.old_threshold:
                fitness *= self.config.old_penalty

            adjusted = fitness/len(self.genomes)
            genome.adjusted_fitness = adjusted
            self.adjusted_sum += adjusted

    def add_genome(self, new_genome):

        added_genome = False

        for i, genome in enumerate(self.genomes):

            if new_genome.adjusted_fitness > genome.adjusted_fitness:
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
        self.adjusted_sum = 0

    def should_go_extinct(self, no_improvement_threshold):
        return self.age_since_improvement > no_improvement_threshold

    def reproduce(self):
        print("calling species.reproduce")
        offspring = [self.breeder.create_genome(self.leader.links)] # Always save species leader.

        best_percent_index = floor(self.config.survival_threshold*len(self.genomes))
        mating_pool = self.genomes[:best_percent_index]

        print(f"expected offspring {self.expected_offspring}")
        while len(offspring) < self.expected_offspring:
            print(f"Entered reproduction loop in species with {len(self.genomes)} members")

            # Some of the time, only mutate.
            if random() < self.config.mutate_only_probability or mating_pool == []:

                if mating_pool == []:
                    parent = self.genomes[0]

                else:
                    parent = choice(mating_pool)

                copy = self.breeder.create_genome()

                success = copy.mutate_structure()

                if not success:
                    copy.mutate_non_structure()

                offspring += [copy]

            # Some of the time, mate.
            else:
                mother = choice(mating_pool)
                father = choice(mating_pool)
                baby = self.breeder.crossover(mother, father)

                offspring.append(baby)

        return offspring
