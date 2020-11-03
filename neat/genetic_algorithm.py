from neat.environment import Environment
from neat.population import Population
from neat.config import Config


class GeneticAlgorithm:

    def __init__(self, config_filename, environment):
        self.population = Population(config=Config(config_filename))
        self.environment = environment

    def run(self):

        while not self.population.stopping_criterion():

            for genome in self.population.genomes:
                fitness, done = self.environment.evaluate(genome)
                genome.original_fitness = fitness

                if done:
                    return

            self.population.speciate_genomes()
            self.population.adjust_fitness_scores()
            self.population.set_spawn_amounts()
            self.population.reproduce()
            self.population.reset()
