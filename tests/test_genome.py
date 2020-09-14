from neat.genome import Genome
from neat.enums.node_types import NodeType
import pytest

@pytest.fixture(name='genome')
def initialised_genome():
    num_inputs = 10
    num_outputs = 10
    genome_id = 1
    genome = Genome(genome_id, num_inputs, num_outputs)
    return genome

@pytest.fixture
def loopable_genome():
    pass

@pytest.fixture
def unloopable_genome():
    pass

@pytest.fixture
def connectable_genome():
    pass


def test_node_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.nodes) == inputs + outputs, "correct number of nodes"
    assert [x.id for x in genome.nodes] == [x for x in range(inputs + outputs)], "correct node labeling"
    assert [x.node_type for x in genome.nodes[:inputs]] == [NodeType.INPUT for x in range(inputs)], "correct type for inputs"
    assert [x.node_type for x in genome.nodes[inputs:]] == [NodeType.OUTPUT for x in range(outputs)], "correct type for outputs"


def test_link_initialisation(genome):
    inputs = genome.num_inputs
    outputs = genome.num_outputs
    assert len(genome.links) == inputs*outputs, "correct number of links"