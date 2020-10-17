from neat.environment import Environment
from neat.population import Population
from neat.config import Config


config = Config("config.json")
environment = Environment()
population = Population(config=config)


while not population.stopping_criterion():

    for genome in population.genomes:
        phenotype = genome.network()
        fitness = environment.evaluate(phenotype)
        genome.fitness = fitness

    population.speciate_genomes()
    population.statistics()
    population.adjust_fitness_scores()
    population.set_spawn_amounts()
    population.reproduce()
    population.reset()
