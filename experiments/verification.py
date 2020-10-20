from neat.genetic_algorithm import GeneticAlgorithm
from experiments.xor import xor

environment = xor()
ga = GeneticAlgorithm(config_filename = "configs/xor_config.json", environment=environment)
ga.run()