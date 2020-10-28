from unittest.mock import Mock
from neat.genome import Genome
from neat.innovation_tracker import InnovationTracker
from math import exp

config = Mock()

config.num_inputs = 1
config.num_outputs = 1

config.node_add_tries = 15
config.link_add_tries = 15
config.link_recurrent_probability = 0.2

config.weight_mutation_probability = 1

config.weight_mutation_rate = 1
config.weight_replacement_rate = 0
config.weight_mutation_power = 0.5

config.population_size = 10

config.c_excess = 1
config.c_disjoint = 1
config.c_weight = 1
config.compatibility_threshold = 4

config.survival_threshold = 0.8
config.young_boost = 1
config.old_penalty = 1
config.old_threshold = 20
config.young_threshold = 10

tracker = InnovationTracker(config)
genome = Genome(id=0, config=config, tracker=tracker)

genome.add_loop_link()
network = genome.network()
assert network.links[-1].from_node.id == 2

def sigmoid(x):
    return 1 / (1 + exp(-x))

output = network.activate(inputs=[0])
assert output == [sigmoid(0)], "correct output"