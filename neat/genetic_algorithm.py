from neat.environment import Environment
from neat.population import Population
from neat.config import Config


class GeneticAlgorithm:

    def __init__(self, environment):
        self.population = Population(config=Config("config.json"))
        self.environment = environment

    def run(self):

        while not self.population.stopping_criterion():

            for genome in self.population.genomes:
                phenotype = genome.network()
                genome.fitness = self.environment.evaluate(phenotype)

            self.population.speciate_genomes()
            self.population.adjust_negative_fitness_scores()
            self.population.set_spawn_amounts()
            self.population.reproduce()
            self.population.reset()
