from neat.environment import Environment
from neat.population import Population
from neat.config import Config


config = Config("config.json")
environment = Environment()
population = Population(config=config)


while not population.stopping_criterion():

    for genome in population.genomes:
        phenotype = genome.network()
        genome.fitness = environment.evaluate(phenotype)

    population.speciate_genomes()
    population.adjust_negative_fitness_scores()
    population.set_spawn_amounts()
    population.reproduce()
    population.reset()
