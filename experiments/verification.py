from neat.genetic_algorithm import GeneticAlgorithm
from experiments.logical_or import LogicalOr

environment = LogicalOr()
ga = GeneticAlgorithm(config_filename = "configs/xor_config.json", environment=environment)
ga.run()
