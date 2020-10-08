from neat.environment import Environment
from neat.population import Population
from neat.innovation_tracker import InnovationTracker
from neat.breeder import Breeder


class GeneticAlgorithm:

    def __init__(self):
        self.environment = Environment()
        self.population = Population()
        self.tracker = InnovationTracker()
        self.breeder = Breeder()

    def generation_step(self):

        # Create networks
        # Evaluate networks
        # Select parents
        # Crossover and mutations
        pass

    def read_config(self):
        pass