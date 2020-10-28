from neat.genetic_algorithm import GeneticAlgorithm
from experiments.logical_xor import LogicalXor

environment = LogicalXor()
ga = GeneticAlgorithm(config_filename = "configs/xor_config.json", environment=environment)
ga.run()
