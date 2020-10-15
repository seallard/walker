from neat.genome import Genome
from neat.enums.node_types import NodeType
from neat.innovation_tracker import InnovationTracker
from neat.breeder import Breeder
import pytest
from unittest.mock import Mock


@pytest.fixture()
def standard_config():
    config = Mock()
    config.num_inputs = 1
    config.num_outputs = 1
    config.node_add_tries = 15
    config.link_add_tries = 15
    config.loop_add_tries = 15
    config.weight_mutation_rate = 1
    config.weight_replacement_rate = 0
    config.weight_mutation_range = 0.5
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
    return config

@pytest.fixture()
def multiple_inputs_config(standard_config):
    standard_config.num_inputs = 2
    return standard_config


@pytest.fixture()
def multiple_input_output_config(multiple_inputs_config):
    multiple_inputs_config.num_outputs = 2
    return multiple_inputs_config


@pytest.fixture()
def genome(standard_config):
    return Genome(id=0, config=standard_config)


@pytest.fixture
def loopable_genome(genome):
    for node in genome.nodes:
        node.type = NodeType.HIDDEN
    return genome


@pytest.fixture
def unloopable_genome(genome):
    for node in genome.nodes:
        node.type = NodeType.BIAS
    return genome


@pytest.fixture
def connectable_genome(standard_config):
    genome = Genome(id=1, config=standard_config)
    genome.links = []
    return genome


@pytest.fixture
def make_recurrent_genome(standard_config, tracker):
    genome = Genome(id=1, config=standard_config)
    genome.config.link_add_tries = 50
    genome.mutate_add_node(tracker)
    genome.nodes[-1].id = 2
    genome.links[-2].id = 1
    genome.links[-1].id = 2

    return genome


@pytest.fixture
def tracker(standard_config):
    return InnovationTracker(standard_config)

@pytest.fixture
def breeder(standard_config):
    return Breeder(standard_config)
