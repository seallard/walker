from neat.genetic_algorithm import GeneticAlgorithm
from experiments.logical_xor import LogicalXor

environment = LogicalXor()

for i in range(100):
    print(f"Run {i}")
    ga = GeneticAlgorithm(config_filename = "configs/xor_config.json", environment=environment)

    ga.run()

environment.stats()